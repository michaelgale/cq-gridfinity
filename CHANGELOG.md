## Changelog

- v.0.1.0 - Initial release
- v.0.1.1 - fixed release
- v.0.2.0 - Added new "lite" style box
- v.0.2.1 - Added new unsupported magnet hole types
- v.0.2.2 - Added SVG export and integrated STL exporter
- v.0.2.3 - Updated to python build tools to make distribution
- v.0.3.0 - Added console generator scripts: gridfinitybox and gridfinitybase
- v.0.4.0 - Added `GridfinityRuggedBox` class and `ruggedbox` console script. Various other improvements.
- v.0.4.1 - Fixed docstring in `__init__.py`
- v.0.4.2 - Improved script automatic renaming
- v.0.4.3 - Fixed regression bug with using multilevel extrusion functions from cq-kit
- v.0.4.4 - IMPORTANT FIX: generated geometry breaks using CadQuery v.2.4+ due to changes in CadQuery's `extrude` method.  This version should work with any CQ version since it detects which CQ extrusion implementation is used at runtime.
