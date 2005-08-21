Oficjalne repo polskiego projektu tłumaczenia dokumentacji.

Zasady:

1. Zakaz mieszania w cudzych katalogach, każdy ma własny lub powinien takowy
utworzyć. (svn mkdir <username>, svn commit)
2. Zawsze xmllint --valid --noout przed svn commit
3. W htdocs są wszystkie polskie pliki z gentoo.org, nie ma sensu tam mieszać,
kopiujemy plik do własnego katalogu, commitujemy (svn add file.xml, svn commit),
zmieniamy, commitujemy znowu.
4. Have fun.
