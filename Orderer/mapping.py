class Named_Map():
    def __init__(self, name, _map):
        self.name = name
        self.map = _map

    def __repr__(self):
        return str(self.map)

    def __setitem__(self, key, value):
        self.map[key] = value

    def __getitem__(self, item):
        return self.map[item]
    
    def __iter__(self):
        return iter(self.map.items())
   
    def __len__(self):
        return len(self.map)

    
personal_map = {
	"Trash" : [".png", ".bat", ".jpg", ".msg", ".lnk", ".html", ".pptx", '.ico', '.txt', ".oft", ".docx", ".doc", ".zip",".7z", ".PNG", ".emz", ".pst", ".eml", ".rar", ".swf", ".ics"],
	"Installs" : [".exe", ".rdp", ".msi"],
	"Diagrams" : [".vsdx"],
	"Data" : [".csv", ".xlsx", ".xlsm", ".xls", ".json", ".xml", ".evtx", ".json", "json-formatted"],
	"Documents" : [".pdf", ".ppsx"],
	"Python Packages" : [".whl", ".tar.gz"],
	"Scripts" : [".py", ".pac", ".js", ".sql", ".sh"],
	"Videos" : [".mp4"],
        "Code" : [".cpp", ".c", ".h"],
        "No Type" : []
	}

general_map = {
    "Text Files": [ ".DOC",".DOCX",".LOG",".MSG",".ODT",".PAGES",".RTF",".TEX",".TXT",".WPD",".WPS"],
    "Data Files": [ ".CSV", ".DAT", ".GED", ".KEY", ".KEYCHAIN", ".PPS", ".PPT", ".PPTX", ".SDF", ".TAR", ".TAX2016", ".TAX2018", ".VCF", ".XML"   ],
    "Audio Files": [ ".AIF", ".IFF", ".M3U", ".M4A", ".MID", ".MP3", ".MPA", ".WAV", ".WMA"   ],
    "Video Files": [ ".3G2", ".3GP", ".ASF", ".AVI", ".FLV", ".M4V", ".MOV", ".MP4", ".MPG", ".RM", ".SRT", ".SWF", ".VOB", ".WMV"   ],
    "3D Image Files": [ ".3DM", ".3DS", ".MAX", ".OBJ"   ],
    "Raster Image Files": [ ".BMP", ".DDS", ".GIF", ".HEIC", ".JPG", ".PNG", ".PSD", ".PSPIMAGE", ".TGA", ".THM", ".TIF", ".TIFF", ".YUV"   ],
    "Vector Image Files": [ ".AI", ".EPS", ".PS", ".SVG"   ],
    "Page Layout Files": [ ".INDD", ".PCT", ".PDF"   ],
    "Spreadsheet Files": [ ".XLR", ".XLS", ".XLSX"   ],
    "Database Files": [ ".ACCDB", ".DB", ".DBF", ".MDB", ".PDB", ".SQL"   ],
    "Executable Files": [ ".APK", ".APP", ".BAT", ".CGI", ".COM", ".EXE", ".GADGET", ".JAR", ".WSF"   ],
    "Game Files": [ ".B", ".DEM", ".GAM", ".NES", ".ROM", ".SAV"   ],
    "CAD Files": [ ".DWG", ".DXF"   ],
    "GIS Files": [ ".GPX", ".KML", ".KMZ"   ],
    "Web Files": [ ".ASP", ".ASPX", ".CER", ".CFM", ".CSR", ".CSS", ".DCR", ".HTM", ".HTML", ".JS", ".JSP", ".PHP", ".RSS", ".XHTML"   ],
    "Plugin Files": [ ".CRX", ".PLUGIN"   ],
    "Font Files": [ ".FNT", ".FON", ".OTF", ".TTF"   ],
    "System Files": [ ".CAB", ".CPL", ".CUR", ".DESKTHEMEPACK", ".DLL", ".DMP", ".DRV", ".ICNS", ".ICO", ".LNK", ".SYS"   ],
    "Settings Files": [ ".CFG", ".INI", ".PRF"   ],
    "Encoded Files": [ ".HQX", ".MIM", ".UUE"   ],
    "Compressed Files": [ ".7Z", ".CBR", ".DEB", ".GZ", ".PKG", ".RAR", ".RPM", ".SITX", ".TAR.GZ", ".ZIP", ".ZIPX"   ],
    "Disk Image Files": [ ".BIN", ".CUE", ".DMG", ".ISO", ".MDF", ".TOAST", ".VCD"   ],
    "Developer Files": [ ".C", ".CLASS", ".CPP", ".CS", ".DTD", ".FLA", ".H", ".JAVA", ".LUA", ".M", ".PL", ".PY", ".SH", ".SLN", ".SWIFT", ".VB", ".VCXPROJ", ".XCODEPROJ"   ],
    "Backup Files": [ ".BAK", ".TMP"   ],
    "Misc Files": [ ".CRDOWNLOAD", ".ICS", ".MSI", ".PART", ".TORRENT"   ]
}

personal_map = Named_Map('personal_map', personal_map)
general_map = Named_Map('general_map', general_map)

available_maps = [personal_map, general_map]
