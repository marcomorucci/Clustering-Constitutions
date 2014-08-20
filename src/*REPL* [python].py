Python 2.7.5 (default, Mar  9 2014, 22:15:05) 
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import main
working directory: /Users/marco/Copy/projects/constitutions/src
/Library/Python/2.7/site-packages/scipy/spatial/__init__.py:90: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility
  from .ckdtree import *
/Library/Python/2.7/site-packages/scipy/spatial/__init__.py:90: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility
  from .ckdtree import *
/Library/Python/2.7/site-packages/scipy/spatial/__init__.py:91: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility
  from .qhull import *
/Library/Python/2.7/site-packages/scipy/spatial/__init__.py:91: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility
  from .qhull import *
/Library/Python/2.7/site-packages/scipy/interpolate/interpolate.py:28: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility
  from . import _ppoly
/Library/Python/2.7/site-packages/scipy/interpolate/interpolate.py:28: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility
  from . import _ppoly
>>> d = main.run_analysis()
Loading dataset...
Obtaining democracy scores...
Loaded workbook with:  1 sheets.
Running clustering analysis...
Variance explained after LSA: 95.24 %
Preprocessing data...
Variance explained after LSA: 95.24 %
Clustering data...
Cluster homogeneity score (v-measure): 0.0350661092508
Obtaining Judicial Independence scores...
/Library/Python/2.7/site-packages/pandas/core/indexing.py:389: SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_index,col_indexer] = value instead
  self.obj[item] = s
Obtaining State Fragility scores...
Loaded workbook with:  1 sheets.
Generating most used words table...
   cluster         law     person       court      office  constitution  \
0        0  177.333333  153.47619  146.190476  144.333333    117.095238   
1        1  169.987500  101.32500  101.812500  108.475000    111.312500   
2        2  118.128571    0.00000   47.642857   27.442857     50.985714   

        state      public   president  parliament     ...        service  \
0  110.000000  104.000000   99.595238   94.190476     ...      56.571429   
1  105.387500   98.787500  120.912500   77.275000     ...       0.000000   
2   88.257143   59.257143   79.814286   32.242857     ...       0.000000   

     national  commission   republic      right     rights  constitutional  \
0   56.452381     55.5000   0.000000   0.000000   0.000000        0.000000   
1  115.887500     63.2125  75.337500  57.325000  48.300000        0.000000   
2   80.814286      0.0000  71.585714  41.542857  35.057143       29.571429   

        laws  case    general  
0   0.000000   0.0   0.000000  
1   0.000000   0.0   0.000000  
2  25.242857  23.4  22.642857  

[3 rows x 28 columns]
Generating descriptive statistics table...
  cluster fh_score_mean fh_score_median fh_score_std   LJI_mean LJI_median  \
0       0      2.666667             2.5     1.713172  0.7027905    0.82495   
1       1         3.925               4     2.059403   0.525185     0.5029   
2       2      3.085714               3       1.8237  0.4406386     0.3997   

     LJI_std fragility_mean fragility_median fragility_std  
0  0.2798063       6.592593                4      5.712734  
1  0.3249651       7.957143                7      6.314088  
2  0.2622604       10.12121               10      6.125646  
Loaded workbook with:  2 sheets.
Running regressions...
analyze.py:75: SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_index,col_indexer] = value instead
  c_frag[['fragility']] = c_frag['fragility'].astype(float)
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x1123a1510>
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x11253fed0>
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x112309b10>
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x112309ed0>
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x112315b50>
<statsmodels.regression.linear_model.RegressionResultsWrapper object at 0x1122f3650>
>>> d.df
                     country_id  well  law  national  state  provisions  \
0                   Afghanistan   116  108        92     83          79   
1                       Albania    22  149        16     96           5   
2                       Algeria    14   21        95     68          19   
3                       Andorra    13   72         8     31           6   
4                        Angola    14  317       241    209          16   
5             Antigua & Barbuda     1  192         5     13         133   
6                     Argentina     6   61        48     20           5   
7                       Armenia    27  158       166     74          11   
8                     Australia     1   75         0    223          17   
9                       Austria    87  390       277     60         106   
10                   Azerbaijan    12  111         8    116           7   
11                      Bahamas     0  190        16      7         149   
12                      Bahrain     1  121        53     67          37   
13                   Bangladesh     0  194        20     58          78   
14                     Barbados     3  170        14      8         122   
15                      Belarus    16  129        40    124           7   
16                      Belgium    34  245         5     31          21   
17                       Belize     0  215       139     21         138   
18                        Benin    16   71       131     63           9   
19                       Bhutan     6   57       111     53          17   
20                      Bolivia    58  269        28    445           2   
21           Bosnia-Herzegovina     1   25         8      8           3   
22                     Botswana     2  160       126      9          96   
23                       Brazil    80  562       260    266         154   
24                       Brunei     3   47         3     20          24   
25                     Bulgaria     7  122       181     84           9   
26                 Burkina Faso    13  109        57     41          13   
27                      Burundi    25  131       228     48           9   
28                     Cambodia     3   60       129     65           5   
29                     Cameroon    12   68        85     48          11   
..                          ...   ...  ...       ...    ...         ...   
162                 Saint Lucia     0  199         4     10         135   
163  Saint Vincent & Grenadines     0  186         4      7         121   
164                       Sudan     6  162       524    208          48   
165                    Suriname    10  136       123     98          17   
166                   Swaziland     8  283        25     50         144   
167                      Sweden     9  433        46     90         309   
168                 Switzerland     0   61        25     16          21   
169                       Syria     1   79        24     54          17   
170                      Taiwan     2   86        67     53          36   
171                  Tajikistan     6   68         9     81           1   
172                    Tanzania     5  221       168     42         290   
173                    Thailand    25  211       260    306         124   
174                        Togo    13   83       108     56          10   
175                       Tonga     0   69         1      3           5   
176           Trinidad & Tobago     2   80         1     27          79   
177                     Tunisia    12  107        34     65          25   
178                      Turkey     3  286       226    210          91   
179                Turkmenistan     8   62        21     75           4   
180                      Tuvalu     5  161         7    128          73   
181                      Uganda     9  205        61    113         103   
182                     Ukraine     5  141        91    183           4   
183        United Arab Emirates     0   94        44      6          38   
184               United States     2   38    
     0     79           1   
185                     Uruguay    26  168        47     63          64   
186                  Uzbekistan    23   56         7     75           2   
187                     Vanuatu     0   36        30     17           6   
188                   Venezuela    59  414       357    211          45   
189                       Yemen     7  115        23     61           9   
190                      Zambia     1  188       238     35          66   
191                    Zimbabwe     3  179       255    171          24   

     afghanistan  assembly  house  president    ...      vcondoning  venda  \
0             77        70     68         67    ...               0      0   
1              0       139      0         94    ...               0      0   
2              0        50      0        105    ...               0      0   
3              0         1      0          1    ...               0      0   
4              0       108      1        133    ...               0      0   
5              0         4    260         30    ...               0      0   
6              0         1      0         59    ...               0      0   
7              0       149      0        114    ...               0      0   
8              0         0     98         14    ...               0      0   
9              0        27      1        151    ...               0      0   
10             0         2      0        121    ...               0      0   
11             0       114    181         47    ...               0      0   
12             0        35      0         20    ...               0      0   
13             0        27      3        180    ...               0      0   
14             0        78    130         34    ...               0      0   
15             0         2     85        108    ...               0      0   
16             0        10     84         13    ...               0      0   
17             0       124    230         54    ...               0      0   
18             0       123      1        123    ...               0      0   
19             0        42     26          0    ...               0      0   
20             0       110      0         75    ...               0      0   
21             0        42     21          3    ...               0      0   
22             0       238     61        256    ...               0      0   
23             0        18      5        131    ...               0      0   
24             0         0      0          0    ...               0      0   
25             0       148      0         82    ...               0      0   
26             0        49      0         91    ...               0      0   
27             0       108      0        150    ...               0      0   
28             0       149      1         37    ...               0      0   
29             0        72      1        122    ...               0      0   
..           ...       ...    ...        ...    ...             ...    ...   
162            0         5    227         47    ...               0      0   
163            0         9    170          0    ...               0      0   
164            0        64      0        232    ...               0      0   
165            0       111      0         68    ...               0      0   
166            0        33    171         74    ...               0      0   
167            0         8      8          0    ...               0      0   
168            0         2     13          5    ...               0      0   
169            0        91      0         79    ...               0      0   
170            0        40      0        162    ...               0      0   
171            0         0      0         54    ...               0      0   
172            0       155     39        330    ...               0      0   
173            0       178    377        232    ...               0      0   
174            0        79      0         77    ...               0      0   
175            0       103      5          0    ...               0      0   
176            0        14    265        254    ...               0      0   
177            0       147      0        114    ...               0      0   
178            0       228      2        109    ...               0      0   
179            0         2      0         42    ...               0      0   
180            0         7      0          0    ...               0      0   
181            0        27      0        305    ...               0      0   
182            0         1      1        103    ...               0      0   
183            0         1      0         59    ...               0      0   
184            0         0     33        110    ...               0      0   
185            0        85      1         92    ...               0      0   
186            0         2      0         39    ...               0      0   
187            0         6      0         49    ...               0      0   
188            0       156      1        105    ...               0      0   
189            0         0    170         85    ...               0      0   
190            0       235     18        240    ...               0      0   
191            0       157     66        381    ...               1      1   

     vibrancy  vifair  viiallocations  visubject  viticulture  vsystems  \
0           0       0               0          0            0         0   
1           0       0               0          0            0         0   
2           0       0               0          0            0         0   
3           0       0               0          0            0         0   
4           0       0               0          0            0         0   
5           0       0               0          0            0         0   
6           0       0               0          0            0         0   
7           0       0               0          0            0         0   
8           0       0               0          0            0         0   
9           0       0               0          0            0         0   
10          0       0               0          0            0         0   
11          0       0               0          0            0         0   
12          0       0               0          0            0         0   
13          0       0               0          0            0         0   
14          0       0               0          0            0         0   
15          0       0               0          0            0         0   
16          0       0               0          0            0         0   
17          0       0               0          0            0         0   
18          0       0               0          0            0         0   
19          0       0               0          0            0         0   
20          0       0               0          0            0         0   
21          0       0               0          0            0         0   
22          0       0               0          0            0         0   
23          0       0               0          0            0         0   
24          0       0               0          0            0         0   
25          0       0               0          0            0         0   
26          0       0               0          0            0         0   
27          0       0               0          0            0         0   
28          0       0               0          0            0         0   
29          0       0               0          0            0         0   
..        ...     ...             ...        ...          ...       ...   
162         0       0               0          0            0         0   
163         0       0               0          0            0         0   
164         0       0               0          0            0         0   
165         0       0               0          0            0         0   
166         0       0               0          0            0         0   
167         0       0               0          0            0         0   
168         0       0               0          0            0         0   
169         0       0               0          0            0         0   
170         0       0               0          0            0         0   
171         0       0               0          0            0         0   
172         0       0               0          0            0         0   
173         0       0               0          0            0         0   
174         0       0               0          0            0         0   
175         0       0               0          0            0         0   
176         0       0               0          0            0         0   
177         0       0               0          0            0         0   
178         0       0               0          0            0         0   
179         0       0               0          0            0         0   
180         0       0               0          0            0         0   
181         0       0               0          0            0         0   
182         0       0               0          0            0         0   
183         0       0               0          0            0         0   
184         0       0               0          0            0         0   
185         0       0               0          0            0         0   
186         0       0               0          0            0         0   
187         0       0               0          0            0         0   
188         0       0               0          0            0         0   
189         0       0               0          0            0         0   
190         0       0               0          0            0         0   
191         1       1               1          1            1         1   

     vtheir  xhosa  
0         0      0  
1         0      0  
2         0      0  
3         0      0  
4         0      0  
5         0      0  
6         0      0  
7         0      0  
8         0      0  
9         0      0  
10        0      0  
11        0      0  
12        0      0  
13        0      0  
14        0      0  
15        0      0  
16        0      0  
17        0      0  
18        0      0  
19        0      0  
20        0      0  
21        0      0  
22        0      0  
23        0      0  
24        0      0  
25        0      0  
26        0      0  
27        0      0  
28        0      0  
29        0      0  
..      ...    ...  
162       0      0  
163       0      0  
164       0      0  
165       0      0  
166       0      0  
167       0      0  
168       0      0  
169       0      0  
170       0      0  
171       0      0  
172       0      0  
173       0      0  
174       0      0  
175       0      0  
176       0      0  
177       0      0  
178       0      0  
179       0      0  
180       0      0  
181       0      0  
182       0      0  
183       0      0  
184       0      0  
185       0      0  
186       0      0  
187       0      0  
188       0      0  
189       0      0  
190       0      0  
191       1      1  

[192 rows x 34810 columns]
>>> >>> 
>>> d.topWords
   cluster         law     person       court      office  constitution  \
0        0  177.333333  153.47619  146.190476  144.333333    117.095238   
1        1  169.987500  101.32500  101.812500  108.475000    111.312500   
2        2  118.128571    0.00000   47.642857   27.442857     50.985714   

        state      public   president  parliament     ...        service  \
0  110.000000  104.000000   99.595238   94.190476     ...      56.571429   
1  105.387500   98.787500  120.912500   77.275000     ...       0.000000   
2   88.257143   59.257143   79.814286   32.242857     ...       0.000000   

     national  commission   republic      right     rights  constitutional  \
0   56.452381     55.5000   0.000000   0.000000   0.000000        0.000000   
1  115.887500     63.2125  75.337500  57.325000  48.300000        0.000000   
2   80.814286      0.0000  71.585714  41.542857  35.057143       29.571429   

        laws  case    general  
0   0.000000   0.0   0.000000  
1   0.000000   0.0   0.000000  
2  25.242857  23.4  22.642857  

[3 rows x 28 columns]
>>> d.getCluster(0)['country']
1                   Albania
5         Antigua & Barbuda
7                   Armenia
8                 Australia
11                  Bahamas
13               Bangladesh
14                 Barbados
17                   Belize
22                 Botswana
24                   Brunei
25                 Bulgaria
43                   Cyprus
66                   Greece
67                  Grenada
72                    Haiti
76                    India
78                     Iran
81                   Israel
83                  Jamaica
84                    Japan
88                 Kiribati
96                  Liberia
104                Malaysia
108        Marshall Islands
121                   Nauru
123             Netherlands
126                 Nigeria
129                Pakistan
141                 Romania
144                   Samoa
148                  Serbia
149              Seychelles
151               Singapore
155         Solomon Islands
162             Saint Lucia
165                Suriname
167                  Sweden
175                   Tonga
180                  Tuvalu
183    United Arab Emirates
184           United States
187                 Vanuatu
Name: country, dtype: object
>>> d.getCluster(1)['country']
0            Afghanistan
4                 Angola
9                Austria
10            Azerbaijan
12               Bahrain
15               Belarus
21    Bosnia-Herzegovina
23                Brazil
30                Canada
31            Cape Verde
36              Colombia
42                  Cuba
44        Czech Republic
46               Denmark
48              Dominica
...
163    Saint Vincent & Grenadines
164                         Sudan
166                     Swaziland
168                   Switzerland
169                         Syria
172                      Tanzania
173                      Thailand
176             Trinidad & Tobago
178                        Turkey
179                  Turkmenistan
181                        Uganda
182                       Ukraine
188                     Venezuela
190                        Zambia
191                      Zimbabwe
Name: country, Length: 80, dtype: object
>>> d.getCluster(2)['country']
2                      Algeria
3                      Andorra
6                    Argentina
16                     Belgium
18                       Benin
19                      Bhutan
20                     Bolivia
26                Burkina Faso
27                     Burundi
28                    Cambodia
29                    Cameroon
32    Central African Republic
33                        Chad
34                       Chile
35                       China
...
133        Paraguay
135            Peru
139           Qatar
140     South Korea
143          Rwanda
147         Senegal
150    Sierra Leone
154     Vietnam, N.
170          Taiwan
171      Tajikistan
174            Togo
177         Tunisia
185         Uruguay
186      Uzbekistan
189           Yemen
Name: country, Length: 70, dtype: object
>>> d.df[d.df['country_id']=='Albania']['general']
1    23
Name: general, dtype: int64
>>> d.df[d.df['country_id']=='Armenia']['general']
7    20
Name: general, dtype: int64
>>> d.getCluster(0)['country']
1                   Albania
5         Antigua & Barbuda
7                   Armenia
8                 Australia
11                  Bahamas
13               Bangladesh
14                 Barbados
17                   Belize
22                 Botswana
24                   Brunei
25                 Bulgaria
43                   Cyprus
66                   Greece
67                  Grenada
72                    Haiti
76                    India
78                     Iran
81                   Israel
83                  Jamaica
84                    Japan
88                 Kiribati
96                  Liberia
104                Malaysia
108        Marshall Islands
121                   Nauru
123             Netherlands
126                 Nigeria
129                Pakistan
141                 Romania
144                   Samoa
148                  Serbia
149              Seychelles
151               Singapore
155         Solomon Islands
162             Saint Lucia
165                Suriname
167                  Sweden
175                   Tonga
180                  Tuvalu
183    United Arab Emirates
184           United States
187                 Vanuatu
Name: country, dtype: object
>>> d.cdb.boxplot(column="fh_score",by="kmeans")
<matplotlib.axes.AxesSubplot object at 0x1122ead10>
>>> import matplotlib.pyplot as plt
>>> plt.show()
>>> d.cdb.boxplot(column="LJI",by="kmeans")
<matplotlib.axes.AxesSubplot object at 0x1122efb50>
>>> plt.show()
>>> d.cdb.boxplot(column="fh_score",by="kmeans")
<matplotlib.axes.AxesSubplot object at 0x112309950>
>>> plt.show()
>>> d.cdb.boxplot(column="fragility",by="kmeans")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Python/2.7/site-packages/pandas/core/frame.py", line 4973, in boxplot
    **kwds)
  File "/Library/Python/2.7/site-packages/pandas/tools/plotting.py", line 2368, in boxplot
    ax=ax, layout=layout, return_type=return_type)
  File "/Library/Python/2.7/site-packages/pandas/tools/plotting.py", line 2764, in _grouped_plot_by_column
    re_plotf = plotf(keys, values, ax, **kwargs)
  File "/Library/Python/2.7/site-packages/pandas/tools/plotting.py", line 2341, in plot_group
    bp = ax.boxplot(values, **kwds)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/matplotlib/axes.py", line 5541, in boxplot
    q1, med, q3 = mlab.prctile(d,[25,50,75])
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/matplotlib/mlab.py", line 945, in prctile
    return _interpolate(values[ai],values[bi],frac)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/matplotlib/mlab.py", line 919, in _interpolate
    return a + (b - a)*fraction
TypeError: unsupported operand type(s) for -: 'str' and 'str'
>>> d.cdb[d.cdb['fragility'] != 'NA'].boxplot(column="fragility",by="kmeans")
<matplotlib.axes.AxesSubplot object at 0x11250e0d0>
>>> plt.show()
>>> plt.topWords
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'topWords'
>>> d.topWords
   cluster         law     person       court      office  constitution  \
0        0  177.333333  153.47619  146.190476  144.333333    117.095238   
1        1  169.987500  101.32500  101.812500  108.475000    111.312500   
2        2  118.128571    0.00000   47.642857   27.442857     50.985714   

        state      public   president  parliament     ...        service  \
0  110.000000  104.000000   99.595238   94.190476     ...      56.571429   
1  105.387500   98.787500  120.912500   77.275000     ...       0.000000   
2   88.257143   59.257143   79.814286   32.242857     ...       0.000000   

     national  commission   republic      right     rights  constitutional  \
0   56.452381     55.5000   0.000000   0.000000   0.000000        0.000000   
1  115.887500     63.2125  75.337500  57.325000  48.300000        0.000000   
2   80.814286      0.0000  71.585714  41.542857  35.057143       29.571429   

        laws  case    general  
0   0.000000   0.0   0.000000  
1   0.000000   0.0   0.000000  
2  25.242857  23.4  22.642857  

[3 rows x 28 columns]
>>> d.topWords.plot()
<matplotlib.axes.AxesSubplot object at 0x112538c50>
>>> plt.show()
>>> d.topWords.histogram()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Python/2.7/site-packages/pandas/core/generic.py", line 1843, in __getattr__
    (type(self).__name__, name))
AttributeError: 'DataFrame' object has no attribute 'histogram'
>>> d.topWords.hist()
array([[<matplotlib.axes.AxesSubplot object at 0x1117fba50>,
        <matplotlib.axes.AxesSubplot object at 0x111802f10>,
        <matplotlib.axes.AxesSubplot object at 0x1122ac050>,
        <matplotlib.axes.AxesSubplot object at 0x1117fac50>,
        <matplotlib.axes.AxesSubplot object at 0x112862e10>],
       [<matplotlib.axes.AxesSubplot object at 0x1117d01d0>,
        <matplotlib.axes.AxesSubplot object at 0x1117a89d0>,
        <matplotlib.axes.AxesSubplot object at 0x1124c1590>,
        <matplotlib.axes.AxesSubplot object at 0x112140550>,
        <matplotlib.axes.AxesSubplot object at 0x112830950>],
       [<matplotlib.axes.AxesSubplot object at 0x112833fd0>,
        <matplotlib.axes.AxesSubplot object at 0x111698d10>,
        <matplotlib.axes.AxesSubplot object at 0x11169ff90>,
        <matplotlib.axes.AxesSubplot object at 0x112f10110>,
        <matplotlib.axes.AxesSubplot object at 0x112f14f10>],
       [<matplotlib.axes.AxesSubplot object at 0x1114ad4d0>,
        <matplotlib.axes.AxesSubplot object at 0x111666490>,
        <matplotlib.axes.AxesSubplot object at 0x112d08890>,
        <matplotlib.axes.AxesSubplot object at 0x112cf0850>,
        <matplotlib.axes.AxesSubplot object at 0x1125f1c50>],
       [<matplotlib.axes.AxesSubplot object at 0x1125f8ed0>,
        <matplotlib.axes.AxesSubplot object at 0x1147fa050>,
        <matplotlib.axes.AxesSubplot object at 0x1147fef10>,
        <matplotlib.axes.AxesSubplot object at 0x10ee19190>,
        <matplotlib.axes.AxesSubplot object at 0x10ee482d0>],
       [<matplotlib.axes.AxesSubplot object at 0x10ee6b990>,
        <matplotlib.axes.AxesSubplot object at 0x1115f8b90>,
        <matplotlib.axes.AxesSubplot object at 0x11161dd50>,
        <matplotlib.axes.AxesSubplot object at 0x11175bf50>,
        <matplotlib.axes.AxesSubplot object at 0x1118ba150>]], dtype=object)
>>> plt.show()
>>> import build_datasets
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.buildTopWordsTable(thresh=20)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build_datasets.py", line 140, in buildTopWordsTable
    self.topWords.loc[idx, w] = self.getWordAvg(countries, w)
TypeError: getWordAvg() takes exactly 2 arguments (3 given)
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.buildTopWordsTable(thresh=20)
>>> dat.topWords
   cluster         law     person       court      office  constitution  \
0        0  177.333333  153.47619  146.190476  144.333333    117.095238   
1        0  169.987500  101.32500  101.812500  108.475000    111.312500   
2        0  118.128571    0.00000   47.642857   27.442857     50.985714   

        state      public   president  parliament     ...        service  \
0  110.000000  104.000000   99.595238   94.190476     ...      56.571429   
1  105.387500   98.787500  120.912500   77.275000     ...       0.000000   
2   88.257143   59.257143   79.814286   32.242857     ...       0.000000   

     national  commission   republic      right     rights  constitutional  \
0   56.452381     55.5000   0.000000   0.000000   0.000000        0.000000   
1  115.887500     63.2125  75.337500  57.325000  48.300000        0.000000   
2   80.814286      0.0000  71.585714  41.542857  35.057143       29.571429   

        laws  case    general  
0   0.000000   0.0   0.000000  
1   0.000000   0.0   0.000000  
2  25.242857  23.4  22.642857  

[3 rows x 28 columns]
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.buildTopWordsTable(thresh=20)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build_datasets.py", line 142, in buildTopWordsTable
    self.topWords.loc[r, w] = getWordAvg(countries, w)
NameError: global name 'getWordAvg' is not defined
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.buildTopWordsTable(thresh=20)
>>> dat.topWords
   cluster         law     person       court      office  constitution  \
0        0  177.333333  153.47619  146.190476  144.333333    117.095238   
1        1  169.987500  101.32500  101.812500  108.475000    111.312500   
2        2  118.128571    0.00000   47.642857   27.442857     50.985714   

        state      public   president  parliament     ...        service  \
0  110.000000  104.000000   99.595238   94.190476     ...      56.571429   
1  105.387500   98.787500  120.912500   77.275000     ...       0.000000   
2   88.257143   59.257143   79.814286   32.242857     ...       0.000000   

     national  commission   republic      right     rights  constitutional  \
0   56.452381     55.5000   0.000000   0.000000   0.000000        0.000000   
1  115.887500     63.2125  75.337500  57.325000  48.300000        0.000000   
2   80.814286      0.0000  71.585714  41.542857  35.057143       29.571429   

        laws  case    general  
0   0.000000   0.0   0.000000  
1   0.000000   0.0   0.000000  
2  25.242857  23.4  22.642857  

[3 rows x 28 columns]
>>> dat.cdb[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Python/2.7/site-packages/pandas/core/frame.py", line 1678, in __getitem__
    return self._getitem_column(key)
  File "/Library/Python/2.7/site-packages/pandas/core/frame.py", line 1685, in _getitem_column
    return self._get_item_cache(key)
  File "/Library/Python/2.7/site-packages/pandas/core/generic.py", line 1052, in _get_item_cache
    values = self._data.get(item)
  File "/Library/Python/2.7/site-packages/pandas/core/internals.py", line 2565, in get
    loc = self.items.get_loc(item)
  File "/Library/Python/2.7/site-packages/pandas/core/index.py", line 1181, in get_loc
    return self._engine.get_loc(_values_from_object(key))
  File "index.pyx", line 129, in pandas.index.IndexEngine.get_loc (pandas/index.c:3656)
  File "index.pyx", line 149, in pandas.index.IndexEngine.get_loc (pandas/index.c:3534)
  File "hashtable.pyx", line 696, in pandas.hashtable.PyObjectHashTable.get_item (pandas/hashtable.c:11911)
  File "hashtable.pyx", line 704, in pandas.hashtable.PyObjectHashTable.get_item (pandas/hashtable.c:11864)
KeyError: 0
>>> dat.cdb['cluster']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Python/2.7/site-packages/pandas/core/frame.py", line 1678, in __getitem__
    return self._getitem_column(key)
  File "/Library/Python/2.7/site-packages/pandas/core/frame.py", line 1685, in _getitem_column
    return self._get_item_cache(key)
  File "/Library/Python/2.7/site-packages/pandas/core/generic.py", line 1052, in _get_item_cache
    values = self._data.get(item)
  File "/Library/Python/2.7/site-packages/pandas/core/internals.py", line 2565, in get
    loc = self.items.get_loc(item)
  File "/Library/Python/2.7/site-packages/pandas/core/index.py", line 1181, in get_loc
    return self._engine.get_loc(_values_from_object(key))
  File "index.pyx", line 129, in pandas.index.IndexEngine.get_loc (pandas/index.c:3656)
  File "index.pyx", line 149, in pandas.index.IndexEngine.get_loc (pandas/index.c:3534)
  File "hashtable.pyx", line 696, in pandas.hashtable.PyObjectHashTable.get_item (pandas/hashtable.c:11911)
  File "hashtable.pyx", line 704, in pandas.hashtable.PyObjectHashTable.get_item (pandas/hashtable.c:11864)
KeyError: 'cluster'
>>> dat.cdb[
... 
... asd
... 
... 
... 
... 
... q3r3
  File "<stdin>", line 8
    q3r3
       ^
SyntaxError: invalid syntax
>>> dat.cdb['kmeans']
0     1
1     0
2     2
3     2
4     1
5     0
6     2
7     0
8     0
9     1
10    1
11    0
12    1
13    0
14    0
...
177    2
178    1
179    1
180    0
181    1
182    1
183    0
184    0
185    2
186    2
187    0
188    1
189    2
190    1
191    1
Name: kmeans, Length: 192, dtype: int32
>>> dat.getCluster(0)['country']
1                   Albania
5         Antigua & Barbuda
7                   Armenia
8                 Australia
11                  Bahamas
13               Bangladesh
14                 Barbados
17                   Belize
22                 Botswana
24                   Brunei
25                 Bulgaria
43                   Cyprus
66                   Greece
67                  Grenada
72                    Haiti
76                    India
78                     Iran
81                   Israel
83                  Jamaica
84                    Japan
88                 Kiribati
96                  Liberia
104                Malaysia
108        Marshall Islands
121                   Nauru
123             Netherlands
126                 Nigeria
129                Pakistan
141                 Romania
144                   Samoa
148                  Serbia
149              Seychelles
151               Singapore
155         Solomon Islands
162             Saint Lucia
165                Suriname
167                  Sweden
175                   Tonga
180                  Tuvalu
183    United Arab Emirates
184           United States
187                 Vanuatu
Name: country, dtype: object
>>> dat.db[dat.db['country']=="Albania"]['constitutional']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: dataset instance has no attribute 'db'
>>> dat.df[dat.df['country']=="Albania"]['constitutional']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Python/2.7/site-packages/pandas/core/ops.py", line 572, in wrapper
    res = na_op(values, other)
  File "/Library/Python/2.7/site-packages/pandas/core/ops.py", line 541, in na_op
    raise TypeError("invalid type comparison")
TypeError: invalid type comparison
>>> dat.df[dat.df['country_id']=="Albania"]['constitutional']
1    58
Name: constitutional, dtype: int64
>>> a = DataFrame
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'DataFrame' is not defined
>>> from pandas import DataFrame
>>> a = DataFrame({'a':[1,2,3],'b':[4,5,6],'c':[7,8,9]})
>>> a
   a  b  c
0  1  4  7
1  2  5  8
2  3  6  9
>>> a.ix[:,1:]
   b  c
0  4  7
1  5  8
2  6  9
>>> a.ix[:,1:] / a.ix[,1]
  File "<stdin>", line 1
    a.ix[:,1:] / a.ix[,1]
                      ^
SyntaxError: invalid syntax
>>> a.ix[:,1:] / a.ix[:,1]
    0   1   2   b   c
0 NaN NaN NaN NaN NaN
1 NaN NaN NaN NaN NaN
2 NaN NaN NaN NaN NaN
>>> a.ix[:,1:] / a.ix[:,'a']
    0   1   2   b   c
0 NaN NaN NaN NaN NaN
1 NaN NaN NaN NaN NaN
2 NaN NaN NaN NaN NaN
>>> dat.getWordAvg(dat.getCluster(0)['country'],'constitutional')
0
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.getWordAvg(dat.getCluster(0)['country'],'constitutional')
0
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.pyc'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.getWordAvg(dat.getCluster(0)['country'],'constitutional')
0
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.getWordAvg(dat.getCluster(0)['country'],'constitutional')
0
>>> reload(build_datasets)
<module 'build_datasets' from 'build_datasets.py'>
>>> dat = build_datasets.dataset()
>>> dat.df = d.df
>>> dat.cdb = d.cdb
>>> dat.getWordAvg(dat.getCluster(0)['country'],'constitutional')
Afghanistan
Albania
Algeria
Andorra
Angola
Antigua & Barbuda
Argentina
Armenia
Australia
Austria
Azerbaijan
Bahamas
Bahrain
Bangladesh
Barbados
Belarus
Belgium
Belize
Benin
Bhutan
Bolivia
Bosnia-Herzegovina
Botswana
Brazil
Brunei
Bulgaria
Burkina Faso
Burundi
Cambodia
Cameroon
Canada
Cape Verde
Central African Republic
Chad
Chile
China
Colombia
Comoros
Congo (Brazzaville)
Costa Rica
Cote d'Ivoire
Croatia
Cuba
Cyprus
Czech Republic
Congo (Kinshasa)
Denmark
Djibouti
Dominica
Dominican Republic
East Timor
Ecuador
Egypt
El Salvador
Equatorial Guinea
Eritrea
Estonia
Ethiopia
Fiji
Finland
France
Gabon
Gambia, The
Georgia
Germany
Ghana
Greece
Grenada
Guatemala
Guinea
Guinea-Bissau
Guyana
Haiti
Honduras
Hungary
Iceland
India
Indonesia
Iran
Iraq
Ireland
Israel
Italy
Jamaica
Japan
Jordan
Kazakhstan
Kenya
Kiribati
Kosovo
Kuwait
Kyrgyzstan
Laos
Latvia
Lebanon
Lesotho
Liberia
Libya
Liechtenstein
Lithuania
Luxembourg
Macedonia
Madagascar
Malawi
Malaysia
Maldives
Mali
Malta
Marshall Islands
Mauritania
Mauritius
Mexico
Micronesia
Moldova
Monaco
Mongolia
Montenegro
Morocco
Mozambique
Burma
Namibia
Nauru
Nepal
Netherlands
Nicaragua
Niger
Nigeria
Norway
Oman
Pakistan
Palau
Panama
Papua New Guinea
Paraguay
North Korea
Peru
Philippines
Poland
Portugal
Qatar
South Korea
Romania
Russia
Rwanda
Samoa
Sao Tome & Principe
Saudi Arabia
Senegal
Serbia
Seychelles
Sierra Leone
Singapore
Slovakia
Slovenia
Vietnam, N.
Solomon Islands
Somalia
South Africa
South Sudan
Spain
Sri Lanka
Saint Kitts and Nevis
Saint Lucia
Saint Vincent & Grenadines
Sudan
Suriname
Swaziland
Sweden
Switzerland
Syria
Taiwan
Tajikistan
Tanzania
Thailand
Togo
Tonga
Trinidad & Tobago
Tunisia
Turkey
Turkmenistan
Tuvalu
Uganda
Ukraine
United Arab Emirates
United States
Uruguay
Uzbekistan
Vanuatu
Venezuela
Yemen
Zambia
Zimbabwe
0
>>> for c in dat.getCluster(0)['country']: print c
... 
Albania
Antigua & Barbuda
Armenia
Australia
Bahamas
Bangladesh
Barbados
Belize
Botswana
Brunei
Bulgaria
Cyprus
Greece
Grenada
Haiti
India
Iran
Israel
Jamaica
Japan
Kiribati
Liberia
Malaysia
Marshall Islands
Nauru
Netherlands
Nigeria
Pakistan
Romania
Samoa
Serbia
Seychelles
Singapore
Solomon Islands
Saint Lucia
Suriname
Sweden
Tonga
Tuvalu
United Arab Emirates
United States
Vanuatu
>>> dat.getWordAvg([dat.getCluster(0)['country']],'constitutional')
Afghanistan
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build_datasets.py", line 118, in getWordAvg
    if self.df.loc[r, 'country_id'] in countries:
  File "/Library/Python/2.7/site-packages/pandas/core/generic.py", line 692, in __nonzero__
    .format(self.__class__.__name__))
ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
>>> dat.getWordAvg([c for c in dat.getCluster(0)['country']],'constitutional')