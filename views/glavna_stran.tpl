%rebase('osnova')

<h1 class="title">Dobrodošli v evidenco naročil. Kaj vas zanima?</h1>

<ul>
%i = 1
%for izbira, url in izbire:
    <li>
        <a href="{{ url }}">
            {{i}}: {{izbira}}
        </a>
    </li>
    %i += 1
%end
</ul>