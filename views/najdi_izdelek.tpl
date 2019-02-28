%rebase('osnova')

<h1 class="title">Najdeni izdelki:</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>

<form method="post">
Ime: <input type="text" name="ime" value="{{ime}}">
<input type="submit" value="Izpiši">

%poravnave = ['left', 'left', 'center', 'center']
<table border = 5>
    <tr>
        %for poravnava, tip_lastnosti in zip(poravnave, lastnosti):
            <th style='text-align: {{ poravnava }}'>
                {{ tip_lastnosti }}
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

<br />
<button type="submit" formaction="/vrnime na prvo stran/">Vrnime nazaj</button>
<br />

</form>