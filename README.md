# userData_test
This tool was developed as a test, it allows an artist to add users through  a directory by which they can then search/filter and display in multiple  formats.  The tool also has the ability to convert the current data into another file  format and change locations.

The tool was built on Windows for Windows.
It was built using "C:/test" as the directory it was run in and the unit test is coded to that for testing purposes.

The tool supports command line functionality:
```
usage: userDataManager.py [-h] -c {add,display,convert} [-dl DATALOCATION]
              [-f {JSON,YAML}] [-ctf {JSON,YAML}] [-df {JSON,YAML,CSV,Text}]
              [-n NAME] [-ad ADDRESS] [-ph PHONE] [-e EMAIL]

optional arguments:
  -h, --help            show this help message and exit
  -c {add,display,convert}, --cmd {add,display,convert}
                        The function to run the given args through
  -dl DATALOCATION, --dataLocation DATALOCATION
                        Location of data files
  -f {JSON,YAML}, --frmt {JSON,YAML}
                        Format of the data files to read from/write to
  -ctf {JSON,YAML}, --convertToFormat {JSON,YAML}
                        Format to convert the data files to, requires '-c convert'
  -df {JSON,YAML,CSV,Text}, --displayFormat {JSON,YAML,CSV,Text}
                        The format to display entries as
  -n NAME, --name NAME  
                        The name of the entry to adding or the filter to search by
  -ad ADDRESS, --address ADDRESS
                        The address of the entry to adding or the filter to search by
  -ph PHONE, --phone PHONE
                        The phone of the entry to adding or the filter to search by
  -e EMAIL, --email EMAIL
                        The email of the entry to adding or the filter to search by


Here are some example commands:

userDataManager.py -c add -f JSON -n "Bord Schimann" -e "bschimann5g@ow.ly" -ph "887-981-1506" -ad "69093 Killdeer Place"
userDataManager.py -c add -f YAML -n "Hewet Keysel" -e "hkeysel5l@uol.com.br" -ph "947-840-4184" -ad "233 Golden Leaf Circle"
userDataManager.py -c convert -f YAML -ctf JSON
userDataManager.py -c display -e ".*@goog.*"
userDataManager.py -c display -n "Al.*" -df YAML
userDataManager.py -c display -n "Al.*" -df Text
userDataManager.py -c display -ph ".*77.*" -df CSV
userDataManager.py -c display -df Text
