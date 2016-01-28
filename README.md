# Chrocalc

>***NOTE:***  
I found this on my computer, don't really remember when I did it.  
I think it was mostly done from memory, as I've done this before but don't have that source code ...probably why I wrote this.  
Now it's here for postery and such.

I guess you might call it an 'inverse' calculator?  
It's an expression generator.  
...A basic integer arithmetic expression generator.  
In that, it's only capable of using integers (0 to 9), and basic arithmetic operations (multiplication, division, addition, and subtraction) to generate an expression.  
E.g. [ 1 + 5 * 6 ]  
...However, it uses Genetic Algorithm to create the expression.  
...And it creates the expression for a target value, that you would specify. (Although, I did not implement input for some reason, so you just have to edit target value in the source code, and then run the code.)

...Um, that's it, I guess.

Oh, PS. It follows order of operations, and 'reads' left to right. (I.e. Miltiplication and devision, before addition and subtraction.)

### Runnning It

Firstly, get python 3.

Then, open it up, find the entry point, looks like this:

``` Python3
if __name__ == "__main__":
```

You can edit the first few lines to configure it.  
The one you REALLY want is the 'target' one:

``` Python3
target = 1111
```

The other useful one is 'chromosome_length' :
``` Python3
chromosome_length = 50
```
(Shorter is faster, but too short means it could take forever to find a correct expression, or make impossible.)