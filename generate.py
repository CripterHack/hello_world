#!/usr/bin/env python3
"""Synthetic contribution art. Generates files; optionally appends dated empty commits.
Never pushes, rewrites history, changes identity, or overwrites an existing manifest.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess

FONT = {
    'H': ['101','101','111','101','101'],
    'E': ['111','100','110','100','111'],
    'L': ['100','100','100','100','111'],
    'O': ['111','101','101','101','111'],
    'W': ['10001','10001','10101','10101','01010'],
    'R': ['110','101','110','101','101'],
    'D': ['110','101','101','101','110'],
}
YEAR = 2015
GRID_START = dt.date(2014, 12, 28)  # Sunday before the start of 2015
ART_START = dt.date(2015, 2, 8)  # Sunday: first pixel of H
DESIGN_ID = "hello-world-2015-02-08-v2"
COMMIT_PREFIX = f"Synthetic art {DESIGN_ID} pixel ["


def design():
    cells = {}
    column = (ART_START - GRID_START).days // 7
    for word_number, word in enumerate('HELLO WORLD'.split()):
        if word_number:
            column += 2  # plus prior letter separator => 3 blank weeks
        for letter in word:
            for row, line in enumerate(FONT[letter]):  # Sunday-Thursday
                for x, value in enumerate(line):
                    if value == '1':
                        cells[(column + x, row)] = 'letter-' + letter
            column += len(FONT[letter][0]) + 1
    entries = []
    for (week, weekday), kind in sorted(cells.items()):
        date = GRID_START + dt.timedelta(days=week * 7 + weekday)
        entries.append({'date': date.isoformat(), 'timestamp': date.isoformat() + 'T12:00:00+00:00',
                        'week': week, 'weekday': weekday, 'kind': kind, 'commits': 1})
    return entries


def svg(entries):
    active = {(e['week'], e['weekday']): e for e in entries}
    lines = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="220" viewBox="0 0 920 220" role="img" aria-labelledby="title desc">',
             '<title id="title">HELLO WORLD — synthetic contribution art, 2015</title>',
             '<desc id="desc">An illustrative calendar, not a screenshot or record of work performed in 2015. Compact HELLO WORLD lettering begins on Sunday, February 8.</desc>',
             '<rect width="920" height="220" rx="12" fill="#0d1117"/>',
             '<text x="22" y="29" fill="#e6edf3" font-family="sans-serif" font-size="16">HELLO WORLD · 2015 · generated art</text>']
    for week in range(53):
        for weekday in range(7):
            date = GRID_START + dt.timedelta(days=week * 7 + weekday)
            if date.year != YEAR:
                continue
            e = active.get((week, weekday))
            color = '#39d353' if e else '#161b22'
            title = date.isoformat() + (' · synthetic pixel' if e else ' · empty')
            lines.append(f'<rect x="{22+week*16}" y="{47+weekday*16}" width="12" height="12" rx="2" fill="{color}"><title>{title}</title></rect>')
    lines += ['<text x="22" y="185" fill="#8b949e" font-family="sans-serif" font-size="12">First letter: 2015-02-08 · Dates are intentionally synthetic · This image is independent of GitHub’s calendar.</text>', '</svg>']
    return '\n'.join(lines) + '\n'


def git(repo, *args, **kwargs):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True, **kwargs).strip()


def append_history(repo, entries):
    repo = repo.resolve()
    if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo:
        raise SystemExit('Choose the repository root explicitly.')
    branch = git(repo, 'branch', '--show-current')
    if branch not in ('master', 'main'):
        raise SystemExit('Checkout the verified default branch (master or main) first.')
    if git(repo, 'status', '--porcelain'):
        raise SystemExit('Working tree must be clean before generating history.')
    name = git(repo, 'config', 'user.name')
    email = git(repo, 'config', 'user.email')
    if not name or not email:
        raise SystemExit('Configure your existing GitHub identity first; prefer your verified noreply address.')
    if COMMIT_PREFIX in git(repo, 'log', '--format=%s'):
        raise SystemExit(f'This design ({DESIGN_ID}) already exists, possibly partially; refusing duplicate generation.')
    # Validation is complete before any mutation. No files are changed by these commits.
    for entry in entries:
        env = dict(os.environ, GIT_AUTHOR_DATE=entry['timestamp'], GIT_COMMITTER_DATE=entry['timestamp'],
                   GIT_AUTHOR_NAME=name, GIT_COMMITTER_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_EMAIL=email)
        git(repo, '-c', 'commit.gpgsign=false', 'commit', '--allow-empty',
            '-m', f"{COMMIT_PREFIX}{entry['date']}] — {entry['kind']}; not historical work", env=env)
    print(f'Created {len(entries)} dated art commits on {branch}. Nothing has been pushed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write preview and date manifest into this directory')
    parser.add_argument('--append-history', type=Path, metavar='REPO_ROOT', help='Append dated empty commits to a clean local clone; never pushes')
    args = parser.parse_args()
    entries = design()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        targets = [args.output / 'dates.json', args.output / 'hello-world.svg']
        if any(p.exists() for p in targets):
            raise SystemExit('Output already exists; refusing to overwrite it.')
        targets[0].write_text(json.dumps({'text': 'HELLO WORLD', 'synthetic': True, 'year': YEAR, 'design_id': DESIGN_ID, 'grid_start': GRID_START.isoformat(), 'art_start': ART_START.isoformat(), 'entries': entries}, indent=2) + '\n')
        targets[1].write_text(svg(entries))
    if args.append_history:
        append_history(args.append_history, entries)
    if not args.output and not args.append_history:
        print(json.dumps({'pixels': len(entries), 'start': entries[0]['date'], 'end': entries[-1]['date']}))


if __name__ == '__main__':
    main()
