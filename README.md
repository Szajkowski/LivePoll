# LivePoll
Strona do tworzenia ankiet z aktualizacją na żywo

### Wymagania projektu
Projekt został stworzony korzystając z FastAPI jako backend z wykorzystaniem sqlalchemy do pracy z bazą danych i mapowania obiektów. 

Na samej stronie jest możliwość dodawania, odczytywania ankiet oraz głosowania na nie, ale API obsługuje pełny CRUD. Można go przetestować w automatycznie generowanej przez FastAPI stronce lokalnyadres:8000/docs, gdzie pokazane są wszystkie endpointy oraz schemas. Dodanie tych możliwości do frontendu miałoby sens tylko wtedy, gdyby strona obsługiwała tworzenie konta i dodawanie użytkowników, co na razie postanowiłem pominąć. Niemniej jest to prospekt na przyszłość.

Websockety zostały wykorzystane do aktualizacji ankiet na żywo. Jeśli ktoś zagłosował już w ankiecie i ogląda wyniki, gdy inna osoba zagłosuje wyniki aktualizują się na żywo przez broadcast. Sprawdzanie kto już głosował wykonuje się poprzez odczytanie wartości dodanej do localstorage. Nie jest to dobre rozwiązanie pod względem cyberbezpieczeństwa, ale pozwala na sprawne przetestowanie aplikacji, na przykład otwierając tą samą ankietę w dwóch różnych przeglądarkach i obserwując zmiany pokazywane na żywo. Oczywiście żeby to działało teoretyczni głosujący muszą być w tej samej sieci internetowej. 

Projekt jest stworzony w wirtualnym środowisku venv pycharma. Posiada plik requirements.txt uzyskany poleceniem pip freeze, gdzie podane są wszystkie wymagania do działania projektu. Co więcej w celu jak maksymalnego uproszczenia korzystania z projektu w katalogu głównym został utworzony plik run.cmd, który automatycznie najpierw aktualizuje wszystkie zależności, a potem uruchamia projekt. Wystarczy go uruchomić albo klikając podwójnie, albo wpisując ".\run" w katalogu głównym projektu.

Każda z opracowanych funkcji posiada type annotation oraz dokumentację w postaci docstringów.

Do projektu zostały dodane testy jednostkowe wykorzystujące moduł pytest. Można je wykonać wpisując polecenie ".\venv\Scripts\python.exe -m pytest" w katalogu głównym projektu. Dlaczego odwoływać się do zagnieżdżonego python.exe zamiast aktywować venv? Dlatego, że windows 10 może mieć problem z wykonywaniem skryptów i trzeba się bawić w nadawanie uprawnień. Zrobienie tego w ten sposób pomija ten problem. WAŻNE: testy wykonują się na żywo na bazie danych.

### Jak uruchomić projekt?
1. Należy zainstalować, a następnie otworzyć XAMPP control panel i uruchomić moduł MySQL oraz Apache
2. Wejść na localhost/phpmyadmin i zaimportować podany w katalogu głównym plik livepoll.sql. Baza wraz z 20 przykładami ankiet utworzy się sama. Po tym można opcjonalnie zastopować moduł Apache, nie będzie już potrzebny.
3. Kliknąć dwukrotnie plik run.cmd lub otworzyć go wpisując ".\run" w katalogu głównym projektu.
4. Konsola po uruchomieniu pokazuje adres, na którym działa strona.

### Pozostałe funkcje
Strona posiada też walidacje danych przy tworzeniu ankiety oraz własny errorpage. Front jest stworzony w javascript. 
