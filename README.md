# latex2sympy

latex2sympy parses LaTeX math expressions and converts it into the
equivalent SymPy form.

## Installation

[ANTLR](http://www.antlr.org/) is used to generate the parser:

```
antlr-4.7.2-complete.jar PS.g4 -o gen
```

or

```
java -jar antlr-4.7.2-complete.jar PS.g4 -o gen
```

## Usage

In Python 2.7:

```python
from latex2sympy import process_sympy

process_sympy("\\frac{d}{dx} x^{2}")
# => "diff(x**(2), x)"
```

## Examples

|LaTeX|Image|Generated SymPy|
|-----|-----|---------------|
|`x^{3}`|![](https://latex.codecogs.com/gif.latex?%5CLARGE%20x%5E%7B3%7D)| `x**3`|
|`\frac{d}{dx} |t|x`|![](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cfrac%7Bd%7D%7Bdx%7D%20%7Ct%7Cx)|`Derivative(x*Abs(t), x)`|
|`\sum_{i = 1}^{n} i`|![](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Csum_%7Bi%20%3D%201%7D%5E%7Bn%7D%20i)|`Sum(i, (i, 1, n))`|
|`\int_{a}^{b} \frac{dt}{t}`|![](https://latex.codecogs.com/gif.latex?%5CLARGE%20%5Cint_%7Ba%7D%5E%7Bb%7D%20%5Cfrac%7Bdt%7D%7Bt%7D)|`Integral(1/t, (t, a, b))`|
|`(2x^3 - x + z)|_{x=3}`|![](https://latex.codecogs.com/gif.latex?%5CLARGE%20%282x%5E3%20-%20x%20&plus;%20z%29%7C_%7Bx%3D3%7D)|`z + 51`
|`\variable{x}<\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20x%3Cy%20)|`x<y`
|`\variable{x}>\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%3Ey)|`x>y`
|`\variable{x}\leq\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%5Cleq%20y)|`x<=y`
|`\variable{x}\geq\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%5Cgeq%20y)|`x>=y`
|`\variable{x}=\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%20=%20y)|`Eq(x, y)`
|`\variable{x}\neq\variable{y}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%20%5Cneq%20y%20)|`Ne(x, y)`
|`\land{\variable{x},\variable{y}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%20%5Cland%20y)|`x & y`
|`\lor{\variable{x},\variable{y}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%20%5Clor%20y)| `x or y`
|`\neg{\variable{x}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20x%20%5Cneg%20y)|`~x`
|`\nrt{\variable{x},\variable{n}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%20%5Csqrt%5Bn%5D%7Bx%7D%20)|`x**(1/n)`
|`\equivalence{\variable{a},\variable{b}`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%205%5Cequiv%204)|`Equivalent(a, b)`
|`\variable{x}\open_int\variable{a}\variable{b})`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20x%5Cepsilon%3C2,6%3E%20)|`(x > a) & (x < b)`
|`\variable{x}\close_int\variable{a}\variable{b})`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20x%5Cepsilon%5B2,6%5D)|`(x >= a) & (x <= b)`
|`\variable{x}\lopen_int\variable{a}\variable{b})`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20x%5Cepsilon%3C2,6%5D)|`(x > a) & (x <= y)`
|`\variable{x}\ropen_int\variable{a}\variable{b})`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20x%5Cepsilon%5B2,6%3E)|`(x >= a) & (x < b)`
|`\absolute\variable{p}`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%7C-5%7C)|`Abs(p) `|
|`\summation{\variable{fi},\variable{i},\variable{y},\variable{z}}`|![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20%5Csum_%7Bi=y%7D%5E%7Bz%7Dfi)|`fi*(-y + z + 1)`|## Contributing
|`\union{\variable{a},\variable{b}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20a%20%5Cbigcup%20b)|`a,b`
|`\intersection{\variable{a},\variable{b}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20a%20%5Cbigcap%20%20b)|`a,b`
|`\subset{\variable{a},\variable{a}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20a%20%5Csubseteq%20b)|`[a]`
|`\superset{\variable{a},\variable{a}}`|![](http://latex.codecogs.com/gif.latex?%5Cdpi%7B110%7D%20a%20%5Csupseteq%20b)|`[a]`
Contributors are welcome! Feel free to open a pull request
or an issue.

