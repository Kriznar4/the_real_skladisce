%rebase('osnova')

<h1 class="title">Takole izgleda vaše skladišče:</h1>

<ul>
%for izdelek in izdelki:
    <li>
        {{ izdelek }}
    </li>
%end
</ul>