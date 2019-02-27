%rebase('osnova')

<h1 class="title">Poraba katerega let vas zanima?</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>
<form method="post">
%for leto in leta:
    <input type="submit" value="{{leto}}"> <br />
%end
</form>
