Oficjalne repo polskiego projektu tłumaczenia dokumentacji.

Zasady:

1. Zakaz mieszania w cudzych katalogach, każdy ma własny lub powinien takowy
utworzyć. (svn mkdir <username>, svn commit). Prosze tez nie ruszac www, sa tam
historyczne pliki naszej starej strony internetowej.
2. Zawsze xmllint --valid --noout przed svn commit
3. W htdocs są wszystkie polskie pliki z gentoo.org, nie ma sensu tam mieszać, i
tak nadpisze to przy pierwszej synchronizacji z oficjalnym repo. Jeśli trzeba
nad czyms popracowac, kopiujemy plik do własnego katalogu, commitujemy (svn
add file.xml, svn commit), zmieniamy, commitujemy znowu - i dajemy znac
koordynatorowi, ze poprawiony plik juz na niego czeka.
4. Have fun.
