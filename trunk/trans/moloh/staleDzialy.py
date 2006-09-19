#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : Łukasz Strzygowski
# edit   : Michał Kurgan

import re
import sys

regexps = (

(r'<guide type="newsletter" link="([^"]*)" lang="en">',
 r'<guide type="newsletter" link="\1" lang="pl">'),

(r'<title>Gentoo Weekly Newsletter</title>',
 r'<title>Tygodnik Gentoo</title>'),

(r'<author title="Editor">',
 r'<author title="Redaktor naczelny">'),

(r'<author title="Author">',
 r'<author title="Redaktor">'),

(r'<version>Volume (\d*), Issue (\d*)</version>',
 r'<version>Wolumin \1, numer \2</version>'),

(r'<abstract>This is the Gentoo Weekly Newsletter for the week of ([^.]*).</abstract>',
 r'<abstract>Wydanie Tygodnika Gentoo z \1.</abstract>'),

(r'<title>Gentoo developer moves</title>',
 r'<title>Zmiana statusu deweloperów Gentoo</title>'),

(r'<title>Moves</title>',
 r'<title>Odeszli</title>'),

(r'The following developers recently left the Gentoo project:',
 r'Następujący deweloperzy opuścili projekt Gentoo Linux w minionym tygodniu:'),

(r'<title>Adds</title>',
 r'<title>Przybyli</title>'),

(r'The following developers recently joined the Gentoo project:',
 r'''Następujący deweloperzy przyłączyli się do projektu Gentoo Linux w minionym
tygodniu:'''),

(r'<title>Changes</title>',
 r'<title>Zmienili status</title>'),

(r'The following developers recently changed roles within the Gentoo project:',
 r'''Następujący deweloperzy zmienili w minionym tygodniu pełnioną w projekcie Gentoo
Linux funkcję:'''),

(r'<li><e>none this week</e></li>',
 r'<li><e>Nikt w tym tygodniu</e></li>'),

(r'<title>Gentoo security</title>',
 r'<title>Bezpieczeństwo Gentoo</title>'),

(r'For more information, please see the',
 r'Więcej informacji można znaleźć w'),

(r'GLSA Announcement',
 r'komunikacie GLSA'),

(r'<title>Summary</title>',
 r'<title>Podsumowanie</title>'),

(r'<uri link=([^>]*>)Statistics',
 r'<uri link=\1Statystyki'),

(r'<uri link=([^>]*>)Closed bug ranking',
 r'<uri link=\1Zamknięte bugi'),

(r'<uri link=([^>]*>)New bug rankings',
 r'<uri link=\1Nowe bugi'),

(r'<title>Statistics</title>',
 r'<title>Statystyki</title>'),

(r'The Gentoo community uses Bugzilla \(<uri link="http://bugs.gentoo.org" >bugs.gentoo.org</uri>\) to record and track bugs, notifications, suggestions and other interactions with the development team.  Between (.*) and (.*), activity on the site has resulted in:',
 r'''Społeczność Gentoo używa Bugzilli (<uri
link="http://bugs.gentoo.org/">bugs.gentoo.org</uri>) do zgłaszania i śledzenia
błędów, ogłoszeń, sugestii oraz innych form kontaktu z deweloperami. Pomiędzy
\1 a \2 aktywność w serwisie przedstawiała się następująco:'''),

(r'<li>(\d*) new bugs during this period</li>',
 r'<li>zgłoszono \1 nowych bugów</li>'),

(r'<li>(\d*) bugs closed or resolved during this period</li>',
 r'<li>zamknięto lub rozwiązano \1 bugów</li>'),

(r'<li>(\d*) previously closed bugs were reopened this period</li>',
 r'<li>\1 uprzednio zamkniętych bugów zostało ponownie otwartych</li>'),

(r'<li>(\d*) closed as NEEDINFO/WONTFIX/CANTFIX/INVALID/UPSTREAM during this period</li>',
 r'<li>\1 bugów oznaczono jako NEEDINFO/WONTFIX/CANTFIX/INVALID/UPSTREAM</li>'),

(r'<li>(\d*) bugs marked as duplicates during this period</li>',
 r'<li>\1 raporty o błędach oznaczono jako duplikaty</li>'),

(r'Of the (\d*) currently open bugs: (\d*) are labeled \'blocker\', (\d*) are labeled \'critical\', and (\d*) are labeled \'major\'.',
 r"""Spośród \1 obecnie otwartych bugów: \2 oznaczono jako 'blocker', \3 jako
'critical', a \4 jako 'major'."""),

(r'<title>Closed bug rankings</title>', r'<title>Zamknięte Bugi</title>'),

(r'The developers and teams who have closed the most bugs during this period are:',
 r'''Deweloperzy oraz zespoły, które zamknęły najwięcej bugów w minionym tygodniu,
to:'''),

(r' with (\d*)([^>]*>)closed bugs',
 r' \1 \2zamkniętych bugów'),

(r'<title>New bug rankings</title>',
 r'<title>Nowe Bugi</title>'),

(r'The developers and teams who have been assigned the most new bugs during this period are:',
 r'''Deweloperzy oraz zespoły, którym przydzielono najwięcej bugów w minionym tygodniu,
to:'''),

(r' with (\d*)([^>]*>)new bugs',
 r' \1 \2nowych bugów'),

(r'<title>GWN feedback</title>',
 r'<title>Opinie czytelników</title>'),

(r'''<p>
Please send us your <mail link="gwn-feedback@gentoo.org">feedback</mail> and
help make the GWN better.
</p>''',
 r'''<p>
Jeśli chcesz, aby Tygodnik Gentoo był jeszcze lepszy, podziel się z <mail
link="gwn-feedback@gentoo.org">nami</mail> swoją opinią na jego temat. Uwagi
dotyczące tłumaczenia można zgłaszać na adres <mail
link="moloh@gentoo.org">koordynatora</mail>.
</p>'''),

(r'<title>GWN subscription information</title>',
 r'<title>Subskrypcja Tygodnika Gentoo</title>'),

(r'''<p>
To subscribe to the Gentoo Weekly Newsletter, send a blank e-mail to
<mail
link="gentoo-gwn\+subscribe@gentoo.org">gentoo-gwn\+subscribe@gentoo.org</mail>.
</p>[ ]''',
 r'''<p>
Aby zaprenumerować Tygodnik Gentoo, należy wysłać pustego emaila na adres <mail
link="gentoo-gwn-pl+subscribe@gentoo.org">gentoo-gwn-pl+subscribe@gentoo.org</mail>.
</p>'''),

(r'''<p>
To unsubscribe to the Gentoo Weekly Newsletter, send a blank e-mail to
<mail
link="gentoo-gwn\+unsubscribe@gentoo.org">gentoo-gwn\+unsubscribe@gentoo.org</mail>
from the e-mail address you are subscribed under.
</p>''',
 r'''<p>
Aby zrezygnować z subskrypcji, należy wysłać pustego emaila na adres <mail
link="gentoo-gwn-pl+unsubscribe@gentoo.org">
gentoo-gwn-pl+unsubscribe@gentoo.org</mail> z konta, na które jest
zarejestrowana.
</p>'''),

(r'<title>Other languages</title>',
 r'<title>Inne języki</title>'),

(r'''<p>
The Gentoo Weekly Newsletter is also available in the following languages:
</p>''',
 r'''<p>
Tygodnik Gentoo jest dostępny w następujących językach:
</p>'''),

(r'''<li> <uri link="/news/zh_cn/gwn/gwn.xml">Chinese \(Simplified\)</uri> </li>
<li> <uri link="/news/da/gwn/gwn.xml">Danish</uri> </li>
<li> <uri link="/news/nl/gwn/gwn.xml">Dutch</uri> </li>
<li> <uri link="/news/en/gwn/gwn.xml">English</uri> </li>
<li> <uri link="/news/de/gwn/gwn.xml">German</uri> </li>
<li> <uri link="/news/el/gwn/gwn.xml">Greek</uri> </li>
<li> <uri link="/news/fr/gwn/gwn.xml">French</uri> </li>
<li> <uri link="/news/ko/gwn/gwn.xml">Korean</uri> </li>
<li> <uri link="/news/ja/gwn/gwn.xml">Japanese</uri> </li>
<li> <uri link="/news/it/gwn/gwn.xml">Italian</uri> </li>
<li> <uri link="/news/pl/gwn/gwn.xml">Polish</uri> </li>
<li> <uri link="/news/pt_br/gwn/gwn.xml">Portuguese \(Brazil\)</uri> </li>
<li> <uri link="/news/pt/gwn/gwn.xml">Portuguese \(Portugal\)</uri> </li>
<li> <uri link="/news/ru/gwn/gwn.xml">Russian</uri> </li>
<li> <uri link="/news/es/gwn/gwn.xml">Spanish</uri> </li>
<!-- <li> <uri link="/news/tr/gwn/gwn.xml">Turkish</uri> </li> -->''',
 r'''  <li><uri link="/news/en/gwn/gwn.xml">angielskim</uri></li>
  <li><uri link="/news/zh_cn/gwn/gwn.xml">chińskim (uproszczony)</uri></li>
  <li><uri link="/news/da/gwn/gwn.xml">duńskim</uri></li>
  <li><uri link="/news/fr/gwn/gwn.xml">francuskim</uri></li>
  <li><uri link="/news/el/gwn/gwn.xml">greckim</uri></li>
  <li><uri link="/news/es/gwn/gwn.xml">hiszpańskim</uri></li>
  <li><uri link="/news/nl/gwn/gwn.xml">holenderskim</uri></li>
  <li><uri link="/news/ja/gwn/gwn.xml">japońskim</uri></li>
  <li><uri link="/news/ko/gwn/gwn.xml">koreańskim</uri></li>
  <li><uri link="/news/de/gwn/gwn.xml">niemieckim</uri></li>
  <li><uri link="/news/pl/gwn/gwn.xml">polskim</uri></li>
  <li><uri link="/news/pt_br/gwn/gwn.xml">portugalskim (Brazylia)</uri></li>
  <li><uri link="/news/pt/gwn/gwn.xml">portugalskim (Portugalia)</uri></li>
  <li><uri link="/news/ru/gwn/gwn.xml">rosyjskim</uri></li>
  <li><uri link="/news/it/gwn/gwn.xml">włoskim</uri></li>''')

)

fname = sys.argv[1]
content = file(fname).read()
for old, new in regexps:
	myold = old.replace(' ', r'\s*')
	res = re.compile(myold, re.DOTALL | re.MULTILINE)
	content = res.sub(new, content)
if "-i" in sys.argv: file(fname, "w").write(content)
else: print content
