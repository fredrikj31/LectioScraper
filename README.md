# [Lectio Scraper](https://fredrikj31.github.io/LectioScraper/)

Lectio Scraper is a Python library for web scraping Lectio. **This only works with students. NOT teachers.**

##### What is Lectio?

Lectio is a web-based communication system that schools in Denmark use. 

## Requirements
Lectio Scraper needs these tool and packages to run. You only need PIP if you install Lectio Scraper through the pip installer.

#### Tools:
- [Python 3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

#### Packages:
We have listed the version we built the library with, not sure if the script will work with a newer version of the packages.
- [Requests](https://pypi.org/project/requests/) 2.23.0
- [lxml](https://pypi.org/project/lxml/) 4.5.0
- [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/) 4.6.3


## Installation
You can install Lectio Scraper via 2 methods.

**1.** Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
 
**Disclaimer!** *This normally comes with python.*

```bash
pip install LectioScraper
```

**2.** You can visit our [releases](https://github.com/fredrikj31/LectioScraper/releases) on Github where you can clone the library from there.

## Usage Example

```python
import Lectio

lec = Lectio(lectioUsername, lectioPassword, SchoolId)

lec.getExercises() # Print out your exercises
```

For the full documentation visit the official documentation [here](https://fredrikj31.github.io/LectioScraper/).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Errors/Help
If you encounter any errors or want help with the script, you can always submit an issue on the [Github repository](https://github.com/fredrikj31/LectioScraper/issues), and I will try to help as fast I can.

## License
[MIT](https://choosealicense.com/licenses/mit/)
