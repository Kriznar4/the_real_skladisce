%rebase('osnova')

<h1 class="title">Letna poraba za leto {{leto}}</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>
%poravnave = ['left', 'left', 'right', 'right']
<table border = 5>
    <tr>
        %for poravnava, tip_lastnost in zip(poravnave, tip_lastnosti):
            <th style='text-align: {{ poravnava }}'>
                {{ tip_lastnost }}
            </th>
        %end
    </tr>
    %for izdelek in izdelki:
        <tr>
            %for poravnava, lastnost in zip(poravnave, izdelek):
                <td style='text-align: {{ poravnava }}'>
                    {{ lastnost }}
                </td>
            %end
        </tr>
    %end
</table>

</form>
<form method="post">
<br />
<button type="submit" formaction="/vrnime na prvo stran/">Vrni me nazaj</button>
<br />
</form>