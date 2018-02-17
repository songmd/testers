# Generated by Django 2.0.2 on 2018-02-13 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import estore.imagefieldex
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=32, verbose_name='选项')),
            ],
            options={
                'verbose_name': '选项',
                'verbose_name_plural': '选项',
            },
        ),
        migrations.CreateModel(
            name='AttributeOptionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
            ],
            options={
                'verbose_name': '选项组',
                'verbose_name_plural': '选项组',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=32, verbose_name='描述')),
                ('picture', estore.imagefieldex.ImageFieldEx(upload_to='estorepics', verbose_name='图片')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='名称')),
                ('no', models.CharField(blank=True, max_length=32, null=True, verbose_name='编号')),
                ('bar_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='条码编号')),
                ('rating', models.FloatField(blank=True, editable=False, null=True, verbose_name='评价')),
                ('description', models.TextField(blank=True, help_text='最多500个字符，250个汉字', max_length=512, null=True, verbose_name='文字描述')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='属性名称')),
                ('code', models.CharField(max_length=32, verbose_name='属性编码')),
                ('type', models.CharField(choices=[('text', '文字'), ('integer', '整数'), ('boolean', '是/否'), ('float', '浮点数'), ('richtext', '富文本'), ('date', '日期'), ('datetime', '时间'), ('option', '选项'), ('multi_option', '多选项'), ('entity', '实体'), ('file', '文件'), ('image', '图片')], default='text', max_length=20, verbose_name='类型')),
                ('required', models.BooleanField(default=False, verbose_name='是否必需')),
                ('option_group', models.ForeignKey(blank=True, help_text='如果属性类型是"选项"或者"多选项",需额外选择一个选项组', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes', to='estore.AttributeOptionGroup', verbose_name='选项组')),
            ],
            options={
                'verbose_name': '商品属性',
                'verbose_name_plural': '商品属性',
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='文字')),
                ('value_integer', models.IntegerField(blank=True, null=True, verbose_name='整数')),
                ('value_boolean', models.NullBooleanField(verbose_name='布尔值')),
                ('value_float', models.FloatField(blank=True, null=True, verbose_name='浮点数')),
                ('value_richtext', models.TextField(blank=True, null=True, verbose_name='富文本')),
                ('value_date', models.DateField(blank=True, null=True, verbose_name='日期')),
                ('value_datetime', models.DateTimeField(blank=True, null=True, verbose_name='时间')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estore.ProductAttribute', verbose_name='属性')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_values', to='estore.Product', verbose_name='商品')),
                ('value_multi_option', models.ManyToManyField(blank=True, related_name='multi_valued_attribute_values', to='estore.AttributeOption', verbose_name='多选值')),
                ('value_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estore.AttributeOption', verbose_name='单选值')),
            ],
            options={
                'verbose_name': '商品属性值',
                'verbose_name_plural': '商品属性值集合',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='分类名称')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='estore.ProductCategory', verbose_name='上级分类')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
            },
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='种类名称')),
                ('requires_shipping', models.BooleanField(default=True, verbose_name='是否运送')),
            ],
            options={
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
            },
        ),
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='店铺名称')),
                ('type', models.CharField(blank=True, help_text='自定义店铺类型，32个字符以内', max_length=32, null=True, verbose_name='店铺类型')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='地址')),
                ('phone_num', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系电话')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='纬度')),
                ('description', models.TextField(blank=True, help_text='最多500个字符，250个汉字', max_length=512, null=True, verbose_name='店铺描述')),
                ('icon', estore.imagefieldex.OneToOneFieldEx(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estore.Picture', verbose_name='店铺图标')),
            ],
            options={
                'verbose_name': '店铺',
                'verbose_name_plural': '店铺',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('code', models.TextField()),
                ('linenos', models.BooleanField(default=False)),
                ('language', models.CharField(choices=[('abap', 'ABAP'), ('abnf', 'ABNF'), ('ada', 'Ada'), ('adl', 'ADL'), ('agda', 'Agda'), ('aheui', 'Aheui'), ('ahk', 'autohotkey'), ('alloy', 'Alloy'), ('ampl', 'Ampl'), ('antlr', 'ANTLR'), ('antlr-as', 'ANTLR With ActionScript Target'), ('antlr-cpp', 'ANTLR With CPP Target'), ('antlr-csharp', 'ANTLR With C# Target'), ('antlr-java', 'ANTLR With Java Target'), ('antlr-objc', 'ANTLR With ObjectiveC Target'), ('antlr-perl', 'ANTLR With Perl Target'), ('antlr-python', 'ANTLR With Python Target'), ('antlr-ruby', 'ANTLR With Ruby Target'), ('apacheconf', 'ApacheConf'), ('apl', 'APL'), ('applescript', 'AppleScript'), ('arduino', 'Arduino'), ('as', 'ActionScript'), ('as3', 'ActionScript 3'), ('aspectj', 'AspectJ'), ('aspx-cs', 'aspx-cs'), ('aspx-vb', 'aspx-vb'), ('asy', 'Asymptote'), ('at', 'AmbientTalk'), ('autoit', 'AutoIt'), ('awk', 'Awk'), ('basemake', 'Base Makefile'), ('bash', 'Bash'), ('bat', 'Batchfile'), ('bbcode', 'BBCode'), ('bc', 'BC'), ('befunge', 'Befunge'), ('bib', 'BibTeX'), ('blitzbasic', 'BlitzBasic'), ('blitzmax', 'BlitzMax'), ('bnf', 'BNF'), ('boo', 'Boo'), ('boogie', 'Boogie'), ('brainfuck', 'Brainfuck'), ('bro', 'Bro'), ('bst', 'BST'), ('bugs', 'BUGS'), ('c', 'C'), ('c-objdump', 'c-objdump'), ('ca65', 'ca65 assembler'), ('cadl', 'cADL'), ('camkes', 'CAmkES'), ('capdl', 'CapDL'), ('capnp', "Cap'n Proto"), ('cbmbas', 'CBM BASIC V2'), ('ceylon', 'Ceylon'), ('cfc', 'Coldfusion CFC'), ('cfengine3', 'CFEngine3'), ('cfm', 'Coldfusion HTML'), ('cfs', 'cfstatement'), ('chai', 'ChaiScript'), ('chapel', 'Chapel'), ('cheetah', 'Cheetah'), ('cirru', 'Cirru'), ('clay', 'Clay'), ('clean', 'Clean'), ('clojure', 'Clojure'), ('clojurescript', 'ClojureScript'), ('cmake', 'CMake'), ('cobol', 'COBOL'), ('cobolfree', 'COBOLFree'), ('coffee-script', 'CoffeeScript'), ('common-lisp', 'Common Lisp'), ('componentpascal', 'Component Pascal'), ('console', 'Bash Session'), ('control', 'Debian Control file'), ('coq', 'Coq'), ('cpp', 'C++'), ('cpp-objdump', 'cpp-objdump'), ('cpsa', 'CPSA'), ('cr', 'Crystal'), ('crmsh', 'Crmsh'), ('croc', 'Croc'), ('cryptol', 'Cryptol'), ('csharp', 'C#'), ('csound', 'Csound Orchestra'), ('csound-document', 'Csound Document'), ('csound-score', 'Csound Score'), ('css', 'CSS'), ('css+django', 'CSS+Django/Jinja'), ('css+erb', 'CSS+Ruby'), ('css+genshitext', 'CSS+Genshi Text'), ('css+lasso', 'CSS+Lasso'), ('css+mako', 'CSS+Mako'), ('css+mozpreproc', 'CSS+mozpreproc'), ('css+myghty', 'CSS+Myghty'), ('css+php', 'CSS+PHP'), ('css+smarty', 'CSS+Smarty'), ('cucumber', 'Gherkin'), ('cuda', 'CUDA'), ('cypher', 'Cypher'), ('cython', 'Cython'), ('d', 'D'), ('d-objdump', 'd-objdump'), ('dart', 'Dart'), ('delphi', 'Delphi'), ('dg', 'dg'), ('diff', 'Diff'), ('django', 'Django/Jinja'), ('docker', 'Docker'), ('doscon', 'MSDOS Session'), ('dpatch', 'Darcs Patch'), ('dtd', 'DTD'), ('duel', 'Duel'), ('dylan', 'Dylan'), ('dylan-console', 'Dylan session'), ('dylan-lid', 'DylanLID'), ('earl-grey', 'Earl Grey'), ('easytrieve', 'Easytrieve'), ('ebnf', 'EBNF'), ('ec', 'eC'), ('ecl', 'ECL'), ('eiffel', 'Eiffel'), ('elixir', 'Elixir'), ('elm', 'Elm'), ('emacs', 'EmacsLisp'), ('erb', 'ERB'), ('erl', 'Erlang erl session'), ('erlang', 'Erlang'), ('evoque', 'Evoque'), ('extempore', 'xtlang'), ('ezhil', 'Ezhil'), ('factor', 'Factor'), ('fan', 'Fantom'), ('fancy', 'Fancy'), ('felix', 'Felix'), ('fish', 'Fish'), ('flatline', 'Flatline'), ('forth', 'Forth'), ('fortran', 'Fortran'), ('fortranfixed', 'FortranFixed'), ('foxpro', 'FoxPro'), ('fsharp', 'FSharp'), ('gap', 'GAP'), ('gas', 'GAS'), ('genshi', 'Genshi'), ('genshitext', 'Genshi Text'), ('glsl', 'GLSL'), ('gnuplot', 'Gnuplot'), ('go', 'Go'), ('golo', 'Golo'), ('gooddata-cl', 'GoodData-CL'), ('gosu', 'Gosu'), ('groff', 'Groff'), ('groovy', 'Groovy'), ('gst', 'Gosu Template'), ('haml', 'Haml'), ('handlebars', 'Handlebars'), ('haskell', 'Haskell'), ('haxeml', 'Hxml'), ('hexdump', 'Hexdump'), ('hsail', 'HSAIL'), ('html', 'HTML'), ('html+cheetah', 'HTML+Cheetah'), ('html+django', 'HTML+Django/Jinja'), ('html+evoque', 'HTML+Evoque'), ('html+genshi', 'HTML+Genshi'), ('html+handlebars', 'HTML+Handlebars'), ('html+lasso', 'HTML+Lasso'), ('html+mako', 'HTML+Mako'), ('html+myghty', 'HTML+Myghty'), ('html+ng2', 'HTML + Angular2'), ('html+php', 'HTML+PHP'), ('html+smarty', 'HTML+Smarty'), ('html+twig', 'HTML+Twig'), ('html+velocity', 'HTML+Velocity'), ('http', 'HTTP'), ('hx', 'Haxe'), ('hybris', 'Hybris'), ('hylang', 'Hy'), ('i6t', 'Inform 6 template'), ('idl', 'IDL'), ('idris', 'Idris'), ('iex', 'Elixir iex session'), ('igor', 'Igor'), ('inform6', 'Inform 6'), ('inform7', 'Inform 7'), ('ini', 'INI'), ('io', 'Io'), ('ioke', 'Ioke'), ('irc', 'IRC logs'), ('isabelle', 'Isabelle'), ('j', 'J'), ('jags', 'JAGS'), ('jasmin', 'Jasmin'), ('java', 'Java'), ('javascript+mozpreproc', 'Javascript+mozpreproc'), ('jcl', 'JCL'), ('jlcon', 'Julia console'), ('js', 'JavaScript'), ('js+cheetah', 'JavaScript+Cheetah'), ('js+django', 'JavaScript+Django/Jinja'), ('js+erb', 'JavaScript+Ruby'), ('js+genshitext', 'JavaScript+Genshi Text'), ('js+lasso', 'JavaScript+Lasso'), ('js+mako', 'JavaScript+Mako'), ('js+myghty', 'JavaScript+Myghty'), ('js+php', 'JavaScript+PHP'), ('js+smarty', 'JavaScript+Smarty'), ('jsgf', 'JSGF'), ('json', 'JSON'), ('json-object', 'JSONBareObject'), ('jsonld', 'JSON-LD'), ('jsp', 'Java Server Page'), ('julia', 'Julia'), ('juttle', 'Juttle'), ('kal', 'Kal'), ('kconfig', 'Kconfig'), ('koka', 'Koka'), ('kotlin', 'Kotlin'), ('lagda', 'Literate Agda'), ('lasso', 'Lasso'), ('lcry', 'Literate Cryptol'), ('lean', 'Lean'), ('less', 'LessCss'), ('lhs', 'Literate Haskell'), ('lidr', 'Literate Idris'), ('lighty', 'Lighttpd configuration file'), ('limbo', 'Limbo'), ('liquid', 'liquid'), ('live-script', 'LiveScript'), ('llvm', 'LLVM'), ('logos', 'Logos'), ('logtalk', 'Logtalk'), ('lsl', 'LSL'), ('lua', 'Lua'), ('make', 'Makefile'), ('mako', 'Mako'), ('maql', 'MAQL'), ('mask', 'Mask'), ('mason', 'Mason'), ('mathematica', 'Mathematica'), ('matlab', 'Matlab'), ('matlabsession', 'Matlab session'), ('md', 'markdown'), ('minid', 'MiniD'), ('modelica', 'Modelica'), ('modula2', 'Modula-2'), ('monkey', 'Monkey'), ('monte', 'Monte'), ('moocode', 'MOOCode'), ('moon', 'MoonScript'), ('mozhashpreproc', 'mozhashpreproc'), ('mozpercentpreproc', 'mozpercentpreproc'), ('mql', 'MQL'), ('mscgen', 'Mscgen'), ('mupad', 'MuPAD'), ('mxml', 'MXML'), ('myghty', 'Myghty'), ('mysql', 'MySQL'), ('nasm', 'NASM'), ('ncl', 'NCL'), ('nemerle', 'Nemerle'), ('nesc', 'nesC'), ('newlisp', 'NewLisp'), ('newspeak', 'Newspeak'), ('ng2', 'Angular2'), ('nginx', 'Nginx configuration file'), ('nim', 'Nimrod'), ('nit', 'Nit'), ('nixos', 'Nix'), ('nsis', 'NSIS'), ('numpy', 'NumPy'), ('nusmv', 'NuSMV'), ('objdump', 'objdump'), ('objdump-nasm', 'objdump-nasm'), ('objective-c', 'Objective-C'), ('objective-c++', 'Objective-C++'), ('objective-j', 'Objective-J'), ('ocaml', 'OCaml'), ('octave', 'Octave'), ('odin', 'ODIN'), ('ooc', 'Ooc'), ('opa', 'Opa'), ('openedge', 'OpenEdge ABL'), ('pacmanconf', 'PacmanConf'), ('pan', 'Pan'), ('parasail', 'ParaSail'), ('pawn', 'Pawn'), ('perl', 'Perl'), ('perl6', 'Perl6'), ('php', 'PHP'), ('pig', 'Pig'), ('pike', 'Pike'), ('pkgconfig', 'PkgConfig'), ('plpgsql', 'PL/pgSQL'), ('postgresql', 'PostgreSQL SQL dialect'), ('postscript', 'PostScript'), ('pot', 'Gettext Catalog'), ('pov', 'POVRay'), ('powershell', 'PowerShell'), ('praat', 'Praat'), ('prolog', 'Prolog'), ('properties', 'Properties'), ('protobuf', 'Protocol Buffer'), ('ps1con', 'PowerShell Session'), ('psql', 'PostgreSQL console (psql)'), ('pug', 'Pug'), ('puppet', 'Puppet'), ('py3tb', 'Python 3.0 Traceback'), ('pycon', 'Python console session'), ('pypylog', 'PyPy Log'), ('pytb', 'Python Traceback'), ('python', 'Python'), ('python3', 'Python 3'), ('qbasic', 'QBasic'), ('qml', 'QML'), ('qvto', 'QVTO'), ('racket', 'Racket'), ('ragel', 'Ragel'), ('ragel-c', 'Ragel in C Host'), ('ragel-cpp', 'Ragel in CPP Host'), ('ragel-d', 'Ragel in D Host'), ('ragel-em', 'Embedded Ragel'), ('ragel-java', 'Ragel in Java Host'), ('ragel-objc', 'Ragel in Objective C Host'), ('ragel-ruby', 'Ragel in Ruby Host'), ('raw', 'Raw token data'), ('rb', 'Ruby'), ('rbcon', 'Ruby irb session'), ('rconsole', 'RConsole'), ('rd', 'Rd'), ('rebol', 'REBOL'), ('red', 'Red'), ('redcode', 'Redcode'), ('registry', 'reg'), ('resource', 'ResourceBundle'), ('rexx', 'Rexx'), ('rhtml', 'RHTML'), ('rnc', 'Relax-NG Compact'), ('roboconf-graph', 'Roboconf Graph'), ('roboconf-instances', 'Roboconf Instances'), ('robotframework', 'RobotFramework'), ('rql', 'RQL'), ('rsl', 'RSL'), ('rst', 'reStructuredText'), ('rts', 'TrafficScript'), ('rust', 'Rust'), ('sas', 'SAS'), ('sass', 'Sass'), ('sc', 'SuperCollider'), ('scala', 'Scala'), ('scaml', 'Scaml'), ('scheme', 'Scheme'), ('scilab', 'Scilab'), ('scss', 'SCSS'), ('shen', 'Shen'), ('silver', 'Silver'), ('slim', 'Slim'), ('smali', 'Smali'), ('smalltalk', 'Smalltalk'), ('smarty', 'Smarty'), ('sml', 'Standard ML'), ('snobol', 'Snobol'), ('snowball', 'Snowball'), ('sourceslist', 'Debian Sourcelist'), ('sp', 'SourcePawn'), ('sparql', 'SPARQL'), ('spec', 'RPMSpec'), ('splus', 'S'), ('sql', 'SQL'), ('sqlite3', 'sqlite3con'), ('squidconf', 'SquidConf'), ('ssp', 'Scalate Server Page'), ('stan', 'Stan'), ('stata', 'Stata'), ('swift', 'Swift'), ('swig', 'SWIG'), ('systemverilog', 'systemverilog'), ('tads3', 'TADS 3'), ('tap', 'TAP'), ('tasm', 'TASM'), ('tcl', 'Tcl'), ('tcsh', 'Tcsh'), ('tcshcon', 'Tcsh Session'), ('tea', 'Tea'), ('termcap', 'Termcap'), ('terminfo', 'Terminfo'), ('terraform', 'Terraform'), ('tex', 'TeX'), ('text', 'Text only'), ('thrift', 'Thrift'), ('todotxt', 'Todotxt'), ('trac-wiki', 'MoinMoin/Trac Wiki markup'), ('treetop', 'Treetop'), ('ts', 'TypeScript'), ('tsql', 'Transact-SQL'), ('turtle', 'Turtle'), ('twig', 'Twig'), ('typoscript', 'TypoScript'), ('typoscriptcssdata', 'TypoScriptCssData'), ('typoscripthtmldata', 'TypoScriptHtmlData'), ('urbiscript', 'UrbiScript'), ('vala', 'Vala'), ('vb.net', 'VB.net'), ('vcl', 'VCL'), ('vclsnippets', 'VCLSnippets'), ('vctreestatus', 'VCTreeStatus'), ('velocity', 'Velocity'), ('verilog', 'verilog'), ('vgl', 'VGL'), ('vhdl', 'vhdl'), ('vim', 'VimL'), ('wdiff', 'WDiff'), ('whiley', 'Whiley'), ('x10', 'X10'), ('xml', 'XML'), ('xml+cheetah', 'XML+Cheetah'), ('xml+django', 'XML+Django/Jinja'), ('xml+erb', 'XML+Ruby'), ('xml+evoque', 'XML+Evoque'), ('xml+lasso', 'XML+Lasso'), ('xml+mako', 'XML+Mako'), ('xml+myghty', 'XML+Myghty'), ('xml+php', 'XML+PHP'), ('xml+smarty', 'XML+Smarty'), ('xml+velocity', 'XML+Velocity'), ('xquery', 'XQuery'), ('xslt', 'XSLT'), ('xtend', 'Xtend'), ('xul+mozpreproc', 'XUL+mozpreproc'), ('yaml', 'YAML'), ('yaml+jinja', 'YAML+Jinja'), ('zephir', 'Zephir')], default='python', max_length=100)),
                ('style', models.CharField(choices=[('abap', 'abap'), ('algol', 'algol'), ('algol_nu', 'algol_nu'), ('arduino', 'arduino'), ('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful'), ('default', 'default'), ('emacs', 'emacs'), ('friendly', 'friendly'), ('fruity', 'fruity'), ('igor', 'igor'), ('lovelace', 'lovelace'), ('manni', 'manni'), ('monokai', 'monokai'), ('murphy', 'murphy'), ('native', 'native'), ('paraiso-dark', 'paraiso-dark'), ('paraiso-light', 'paraiso-light'), ('pastie', 'pastie'), ('perldoc', 'perldoc'), ('rainbow_dash', 'rainbow_dash'), ('rrt', 'rrt'), ('tango', 'tango'), ('trac', 'trac'), ('vim', 'vim'), ('vs', 'vs'), ('xcode', 'xcode')], default='friendly', max_length=100)),
                ('highlighted', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='estore.ProductClass', verbose_name='商品种类'),
        ),
        migrations.AddField(
            model_name='product',
            name='attributies',
            field=models.ManyToManyField(blank=True, through='estore.ProductAttributeValue', to='estore.ProductAttribute', verbose_name='属性'),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='estore.ProductCategory', verbose_name='所属分类'),
        ),
        migrations.AddField(
            model_name='product',
            name='pics',
            field=estore.imagefieldex.ManyToManyFieldEx(blank=True, to='estore.Picture', verbose_name='图片'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='estore.ProductClass', verbose_name='种类'),
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='estore.AttributeOptionGroup', verbose_name='选项组'),
        ),
        migrations.AlterUniqueTogether(
            name='productattributevalue',
            unique_together={('attribute', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='attributeoption',
            unique_together={('group', 'option')},
        ),
    ]
