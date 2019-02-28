%rebase('osnova')

<h1 class="title">Dobrodošli v evidenco naročil. Kaj vas zanima?</h1>

<ul>
%i = 1
%for izbira, url in izbire:
    %if izbira == 'novo narocilo' and len(sez_kos) != 0:
        %url = '/novo narocilo2/'
    %end

    <li>
        <a href="{{ url }}">
            {{i}}: {{izbira}}
        </a>
    </li>
    %i += 1
%end
</ul>