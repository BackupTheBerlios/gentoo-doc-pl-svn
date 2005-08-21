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
<title>Polski projekt tłumaczenia dokumentacji Gentoo</title>

<author title="Koordynator">
 <mail link="rane@gentoo.org">Łukasz Damentko</mail>
</author>

<version>1.0.0</version>
<date>#{`date`}</date>

<abstract>
Oficjalna strona polskiego projektu tłumaczenia dokumentacji Gentoo.
</abstract>

<chapter>
<title>Wprowadzenie</title>
<section>
<body>

<p>
Głównym celem polskiego projektu tłumaczenia dokumentacji Gentoo jest
przetłumaczenie jak największej części dokumentacji Gentoo Linux. Umożliwi to
korzystanie z naszej dystrybucji także użytkownikom nie znającym języka
angielskiego lub znającym go słabo. Na tej stronie przedstawiamy status
tłumaczeń oraz wszelkie niezbędne informacje dla ludzi chętnych do współpracy.
</p>

</body>
</section>
</chapter>

<chapter>
<title>Informacje dla tłumaczy</title>
<section>
<body>

<p>
Wszystkie informacje z jakimi powinni zapoznać się tłumacze spisaliśmy w osobnym
<uri link="http://dev.gentoo.org/~rane/jak-tlumaczyc.html">dokumencie</uri>. Jest
on obowiązkową lekturą dla każdego, kto zamierza dołączyć do naszego projektu.
Osoby zainteresowane pomocą w aktualizowaniu dokumentacji powinny zapoznać się z
<uri link="http://dev.gentoo.org/~rane/jak-aktualizowac.html">opisem</uri>
wszystkich czynności jakich trzeba w tym celu dokonać.
</p>

<p>
Po zapoznaniu się z powyższym tekstem wystarczy wysłać zgłoszenie pod adres
<mail>rane@gentoo.org</mail>. Na adres ten można również wysyłać wszelkie
pytania i sugestie dotyczące projektu oraz już przetłumaczonej dokumentacji.
Jest to służbowa skrzynka koordynatora projektu.  
</p>

</body>
</section>
</chapter>

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
wymagają uaktualnienia. W celu przyglądania polskiej dokumentacji Gentoo należy
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

<chapter>
<title>Uczestnicy projektu</title>
<section>
<body>

<p>
Poniżej znajduje się lista osób aktywnie biorących udział w projekcie.
</p>

<table>
  <tr>
    <th>Imię i nazwisko</th>
    <th>Pseudonim</th>
    <th>E-mail</th>
  </tr>
  <tr>
    <ti>Łukasz Damentko</ti><ti>rane</ti><ti>rane@gentoo.org</ti>
  </tr>
  <tr>
    <ti>Karol Wojtaszek</ti><ti>sekretarz</ti><ti>sekretarz@gentoo.org</ti>
  </tr>
  <tr>
    <ti>Robert Muchacki</ti><ti>muchar</ti><ti>muchar@gentoo.org</ti>
  </tr>
  <tr>
    <ti>Paweł Kwiatkowski</ti><ti>yarel</ti><ti>yarel@o2.pl</ti>
  </tr>
  <tr>
    <ti>Damian Kuras</ti><ti>ShadoWW</ti><ti>damian@lezajsk.info</ti>
  </tr>
  <tr>
    <ti>Mateusz Kotyrba</ti><ti>edi15ta</ti><ti>edi15ta@gazeta.pl</ti>
  </tr>
  <tr>
    <ti>Aleksander Kamil Modzelewski</ti><ti>aleander</ti><ti>aleander@gmail.com</ti>
  </tr>
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
