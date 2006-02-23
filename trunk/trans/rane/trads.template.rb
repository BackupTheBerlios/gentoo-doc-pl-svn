#!/usr/bin/ruby

# This script is supposed to be included by main script and defines column
# headers for table of documents and blahblah that comes around it

# Running this script alone will check xml conformance with xmllint

# {langfrom} and {langto} are placeholders,
# they will be replaced by languages at runtime
$ColHeaders = [ "Dokument" ,\
                "Wersja <br/>angielska" ,\
                "Data <br/>modyfikacji" ,\
                "Wersja<br/>polska" ,\
                "Data <br/>modyfikacji" ,\
                "Wersja <br/>tłumaczenia" ,\
                "Diff wersji<br/>angielskich " ,\
                "Wersja <br/> tłumaczona" ,\
                "Tłumacz" ,\
                "Priorytet" ]

$Part1 = <<END_OF_PART_1
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE guide SYSTEM "/dtd/guide.dtd">
<guide lang="pl">
<title>Status polskiego projektu tłumaczenia dokumentacji Gentoo</title>

<author title="Koordynator">
 <mail link="rane@gentoo.org">Łukasz Damentko</mail>
</author>

<version>1.0.0</version>
<date>#{`date`}</date>

<abstract>
Tabela przedstawiająca status polskiego projektu tłumaczenia dokumentacji
Gentoo.
</abstract>

<chapter>
<title>Aktualny status</title>
<section>
<body>

<p>
Wszystkie wymienione poniżej dokumenty opublikowano już na stronie
<uri>http://gentoo.org</uri>. Pełną ich listę można uzyskać pod adresem
<uri>http://www.gentoo.org/doc/pl/list.xml</uri>. Początkujących użytkowników
Gentoo szczególnie gorąco zachęcamy do przeczytania <uri
link="http://gentoo.org/doc/pl/handbook/index.xml">Podręcznika Gentoo</uri>.
</p>

<p>
Poniższa tabela ma charakter informacyjny, jest narzędziem dla uczestników
projektu i pokazuje, które dokumenty już zostały przetłumaczone oraz które
wymagają uaktualnienia. W celu przejrzenia polskiej dokumentacji Gentoo należy
udać się pod jeden z podanych powyżej adresów.
</p>

<note>
Tabela jest generowana za pomocą tego <uri
link="http://dev.gentoo.org/~neysx/trads/trads-doc.html">skryptu</uri>.
</note>

<p>
W tabeli znajdują się następujące informacje:
</p>

<ul>
  <li>Tytuł dokumentu oraz nazwa pliku xml</li>
  <li>Numer wersji angielskiego tekstu oraz data ostatniej jego modyfikacji</li>
  <li>Data ostatniego uaktualnienia oraz numer wersji tłumaczenia tekstu</li>
  <li>Jeśli wersje się różnią, odnośnik do diffa pomiędzy wersjami
  umożliwiającego uaktualnienie tłumaczenia</li>
  <li>Tłumacza oraz numer wersji jaka obecnie jest tłumaczona na język
  polski</li>
  <li>Priorytet dokumentu:
    <ul>
     <li><img src="images/green.png"  /> Dokument jest aktualny</li>
     <li><img src="images/blue.png"   /> Dokument jest w trakcie tłumaczenia lub uaktualniania</li>
     <li><img src="images/yellow.png" /> Dokument mało priorytetowy</li>
     <li><img src="images/orange.png" /> Dokument jest ważny</li>
     <li><img src="images/red.png"    /> Dokument jest bardzo ważny i musi zostać zaktualizowany w pierwszej kolejności</li>
    </ul>
Im większa ilość kolorowych kropek tym bardziej dokument jest nieaktualny.
  </li>
</ul>

</body>
</section>
<section>
<body>
<table>

END_OF_PART_1
$Part2 = <<END_OF_PART_2

</table>

</body>
</section>
</chapter>
</guide>
END_OF_PART_2

if __FILE__ == $0 then
  require 'open3'
  # Validate document with xmllint
  cmd = "xmllint --noout -;echo $?"
  # Run command through pipe
  pi,po,pe = Open3.popen3(cmd)
  pi.puts $Part1
  pi.puts $Part2
  pi.close
  ro=po.readlines
  re=pe.readlines
  po.close; pe.close
  # display error stream on current stderr
  STDERR.puts re
  raise "\n>>> Invalid xml <<<\n" if ro[0]!~/^0$/  
end
