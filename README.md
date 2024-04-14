This is code of my personal wesite, available at [http://mapsaregreat.com/](http://mapsaregreat.com/). Code includes both directly served files such as html and css and code used to create, validate and maintain this site.

Reports about inaccuracies, mistakes, dead links, typos etc are welcomed - either by mailing me at [matkoniecz@gmail.com](mailto:matkoniecz@gmail.com), [creating issues](https://github.com/matkoniecz/mapsaregreat.com/issues) or by submitting PRs.

Repository is located at [https://github.com/matkoniecz/mapsaregreat.com](https://github.com/matkoniecz/mapsaregreat.com). Code with the development version, published on the Internet during tests is at [https://github.com/matkoniecz/matkoniecz.github.io](https://github.com/matkoniecz/matkoniecz.github.io).

# Notes about maintaining, deploying etc.
## Development dependencies

```
cd "code and content not served directly"
pip3 install -r requirements.txt
```

and, due to [weirdness of one dependency](https://github.com/linkchecker/linkchecker/issues/108#issuecomment-898269896)

```
pip3 install git+https://github.com/linkchecker/linkchecker.git
```

## Validation of code

### Fetching tool

[Obtain vnu](https://github.com/matkoniecz/website-checklist/blob/master/validators.md#nu-html-checker) - put jar into `imported-code` folder

### Running

```
find . -name "*.html" -exec java -jar "imported-code/vnu.jar" --also-check-css --also-check-svg --verbose {} \;
find . -name "*.css" -exec java -jar "imported-code/vnu.jar" --also-check-css --also-check-svg --verbose {} \;

cd "code and content not served directly"
python3 custom_validator.py
```

## Updating to the latest lunar assembler

```
cd "code and content not served directly"
python3 lunar_assembler_update.py
```
