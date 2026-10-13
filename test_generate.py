import datetime as dt
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import generate

class DesignTests(unittest.TestCase):
    def test_manifest(self):
        entries=generate.design()
        self.assertEqual(len(entries),98)
        self.assertEqual(entries[0]['date'],'2015-02-08')
        self.assertEqual(entries[-1]['date'],'2015-12-02')
        self.assertEqual(len({e['date'] for e in entries}),len(entries))
        self.assertEqual(entries,sorted(entries,key=lambda e:e['date']))
        for e in entries:
            self.assertEqual(e['commits'],1)
            self.assertEqual(dt.date.fromisoformat(e['date']),generate.GRID_START+dt.timedelta(days=e['week']*7+e['weekday']))
            self.assertLess(e['week'],53)
        data=json.loads(Path(__file__).with_name('dates.json').read_text())
        self.assertEqual(data['entries'],entries)
        self.assertEqual(data['design_id'],generate.DESIGN_ID)
        self.assertEqual(dt.date.fromisoformat(entries[0]['date']).weekday(),6)
        self.assertTrue(all(e['date'].startswith('2015-') for e in entries))
        self.assertTrue(all(e['kind']!='start-marker' for e in entries))
        self.assertEqual(Path(__file__).with_name('hello-world.svg').read_text(),generate.svg(entries))

    def test_history_and_duplicate_protection(self):
        with tempfile.TemporaryDirectory() as root:
            repo=Path(root)
            subprocess.run(['git','init','-q','-b','master',root],check=True)
            generate.git(repo,'config','user.name','Synthetic Art Test')
            generate.git(repo,'config','user.email','test@example.invalid')
            generate.git(repo,'-c','commit.gpgsign=false','commit','-q','--allow-empty','-m','Synthetic art pixel [1995-01-05] — existing legacy art must survive')
            original=generate.git(repo,'rev-parse','HEAD')
            generate.append_history(repo,generate.design())
            self.assertEqual(generate.git(repo,'rev-list','--count','HEAD'),'99')
            self.assertEqual(generate.git(repo,'rev-parse','HEAD~98'),original)
            records=generate.git(repo,'log','--reverse','--format=%aI|%cI',original+'..HEAD').replace('Z','+00:00').splitlines()
            expected=[e['timestamp']+'|'+e['timestamp'] for e in generate.design()]
            self.assertEqual(records,expected)
            with self.assertRaises(SystemExit):
                generate.append_history(repo,generate.design())
            self.assertEqual(generate.git(repo,'rev-list','--count','HEAD'),'99')
            self.assertEqual(generate.git(repo,'status','--porcelain'),'')

if __name__=='__main__': unittest.main()
