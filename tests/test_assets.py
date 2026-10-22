import importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('assets',Path(__file__).parents[1]/'tools/assets.py')
assets=importlib.util.module_from_spec(spec);spec.loader.exec_module(assets)
class AssetsTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.source=self.root/'firmware.tar';self.source.write_bytes(bytes(range(256))*19+b'end')
  self.parts=self.root/'parts';self.payload=assets.split(self.source,self.parts,1024)
  self.manifest=self.parts/'parts.json';self.output=self.root/'joined.tar'
 def save(self):self.manifest.write_text(json.dumps(self.payload))
 def test_roundtrip(self):
  assets.join(self.manifest,self.output);self.assertEqual(self.source.read_bytes(),self.output.read_bytes())
 def test_no_overwrite(self):
  self.output.write_bytes(b'existing')
  with self.assertRaises(FileExistsError):assets.join(self.manifest,self.output)
  self.assertEqual(self.output.read_bytes(),b'existing')
 def test_corrupt_part(self):
  p=self.parts/self.payload['parts'][0]['path'];p.write_bytes(b'X'*p.stat().st_size)
  with self.assertRaises(ValueError):assets.join(self.manifest,self.output)
  self.assertFalse(self.output.exists());self.assertFalse(self.output.with_suffix('.tar.partial').exists())
 def test_missing_part(self):
  (self.parts/self.payload['parts'][0]['path']).unlink()
  with self.assertRaises(ValueError):assets.join(self.manifest,self.output)
 def test_traversal(self):
  for name in ('../outside','/tmp/secret','C:/secret','a\\b','a//b','./file'):
   with self.subTest(name=name),self.assertRaises(ValueError):assets.within(self.root,name)
 def test_duplicate(self):
  self.payload['parts'].append(self.payload['parts'][0]);self.payload['bytes']+=1024;self.save()
  with self.assertRaises(ValueError):assets.join(self.manifest,self.output)
 def test_whole_hash(self):
  self.payload['sha256']='0'*64;self.save()
  with self.assertRaises(ValueError):assets.join(self.manifest,self.output)
  self.assertFalse(self.output.exists())
 def test_existing_partial_preserved(self):
  p=self.output.with_name(self.output.name+'.partial');p.write_bytes(b'other operation')
  with self.assertRaises(FileExistsError):assets.join(self.manifest,self.output)
  self.assertEqual(p.read_bytes(),b'other operation')
 def test_verify(self):
  m=self.root/'assets.json';m.write_text(json.dumps({'files':[{'path':self.source.name,'bytes':self.source.stat().st_size,'sha256':assets.digest(self.source)}]}))
  assets.verify(m,self.root);self.source.write_bytes(b'bad')
  with self.assertRaises(ValueError):assets.verify(m,self.root)
 def test_empty_and_invalid_split(self):
  p=self.root/'empty';p.touch()
  with self.assertRaises(ValueError):assets.split(p,self.root/'empty-parts')
  with self.assertRaises(ValueError):assets.split(self.source,self.root/'invalid',2*1024**3)
 def test_symlink_escape(self):
  with tempfile.TemporaryDirectory() as outside:
   try:(self.root/'escape').symlink_to(outside,target_is_directory=True)
   except OSError:self.skipTest('symlink unavailable')
   with self.assertRaises(ValueError):assets.within(self.root,'escape/file')
if __name__=='__main__':unittest.main()
