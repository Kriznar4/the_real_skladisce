%rebase('osnova')

<h1 class="title">Takole izgleda vaše skladišče:</h1>

<table border = 5>
    <tr>
        %for tip_lastnosti in lastnosti:
            <th>
                {{ tip_lastnosti }}
            </th>
        %end
    </tr>
    %for izdelek in izdelki:
        <tr>
            %for lastnost in izdelek:
                <td>
                    {{ lastnost }}
                </td>
            %end
        </tr>
    %end
</table>