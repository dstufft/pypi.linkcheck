Definitions
===========
* internal: Hosted on PyPI
* external: Not hosted on PyPI
* file link: An url that appears to be an installable file
* direct external: An external link that is linked to directly from PyPI
* spidered external: An external link that requires spidering a homepage or download link
* *any* external link: Some links are available on PyPI for the project, but these are not
* *only* external link: No links are available on PyPI for the project

PyPI Link Checker Stats
============================================================
* internal file links: 159556
* external file links: 17948
* external only file links: 12637
* direct external links: 5783
* direct external only links: 4467
* spidered external links: 12165
* spidered external only links: 8170
* internal file names: 158485
* external file names: 16024
* projects with any external only links: 2581
* projects with only external only links: 1332
* projects with direct external only links: 1750
* projects with spidered external only links: 1507

Top External Link Domains
============================================================
* github.com: 1210
* downloads.tryton.org: 1198
* bitbucket.org: 800
* launchpad.net: 611
* downloads.reviewboard.org: 553
* ftp.livinglogic.de: 446
* downloads.review-board.org: 291
* www.doughellmann.com: 268
* pr.willowgarage.com: 224
* cheeseshop.python.org: 186
* prdownloads.sourceforge.net: 184
* downloads.sourceforge.net: 180
* plone.org: 179
* infrae.com: 178
* biopython.org: 174
* www.boddie.org.uk: 162
* walco.n--tree.net: 161
* www.defuze.org: 156
* samba.org: 122
* tilestache.org: 122

Top Externally Hosted Projects (by # of external links)
======================================================================
* Djblets: 389
* ReviewBoard: 381
* biopython: 162
* aksy: 161
* keepnote: 150
* PyMOTW: 140
* Mercurial: 135
* Silva: 126
* TileStache: 122
* robotframework: 95
* dnspython: 89
* netCDF4: 81
* RBTools: 74
* nesoni: 74
* ll-xist: 68
* pyodbc: 68
* PsychoPy: 67
* pycups: 58
* python-graph: 58
* subvertpy: 55

Resources
=========
* [Stats generation script](https://github.com/dstufft/pypi.linkcheck/blob/master/stats.py)
* [Projects with any files available only externally](https://github.com/dstufft/pypi.linkcheck/blob/master/any_external_projects.json)
* [Projects with only files available only externally](https://github.com/dstufft/pypi.linkcheck/blob/master/only_external_projects.json)
* [Files only availably externally broken down by project](https://raw.github.com/dstufft/pypi.linkcheck/master/external_only_links.json)
* [Projects with linked files only availably by spidering](https://github.com/dstufft/pypi.linkcheck/blob/master/spidered_only_external_projects.json)
* [Projects with linked files only available by direct external links](https://github.com/dstufft/pypi.linkcheck/blob/master/direct_only_external_projects.json)
