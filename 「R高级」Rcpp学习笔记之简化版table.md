#   
「R高级」Rcpp学习笔记之简化版table
[「R高级」Rcpp学习笔记之简化版table - 简书 (jianshu.com)](https://www.jianshu.com/p/04c4da0e0e40)
[[R包开发资料]]
[[R package]]
[[Awesome R]]
[](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Fwww.jianshu.com%2Fu%2F9ea40b5f607a)

[](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Fwww.jianshu.com%2Fu%2F9ea40b5f607a)[![](https://app.yinxiang.com/images/file-generic.png)webp  
1.1 KB  
](https://app.yinxiang.com/shard/s4/nl/16114937/0e0d2fe3-8c25-4bb3-9ae6-a89dddd3556e/res/a7cbddfd-4d6b-4ca9-be59-6a83f5f5c5f5/webp)

[xuzhougeng](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Fwww.jianshu.com%2Fu%2F9ea40b5f607a)[![](https://app.yinxiang.com/shard/s4/nl/16114937/0e0d2fe3-8c25-4bb3-9ae6-a89dddd3556e/res/21defe01-8c38-4fd9-bf71-b341ca3231ec/19c2bea4-c7f7-467f-a032-4fed9acbc55d?resizeSmall&width=832)](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Fwww.jianshu.com%2Fmobile%2Fcreator)

2020.09.12 16:53:03字数 692阅读 239

R语言有一个自带的函数`table`能够统计输入变量中不同元素出现的次数，举个例子

```R
d <- rep(c("A","B","C"), 10)
table(d)
12
```

果子老师曾写一篇推送，自己写了一个简化版的table，比R自带的table 运行的速度更快，如下
#R语法：sapply 
```R
tableGZ <- function(x){
  if(sum(is.na(x)) == 0){
    data <- x
    input <- unique(x, fromLast = TRUE)
    dd <- sapply(input, 
                 function(x) {sum(data==x)})
    names(dd) <- unique(data, fromLast = TRUE)
    dd
  } else{
    data <- x[!is.na(x)]
    input <- unique(x, fromLast = TRUE)
    dd <- sapply(input, function(x){
      sum(data == x)
    })
    dd <- c(dd, sum(is.na(x)))
    names(dd) <- c(input, 'NA')
    dd
  }
}
12345678910111213141516171819
```

我们通过运行1000次代码，来比较下两者的运行速度

```R
bench::system_time(for ( i in 1:1000){
  tableGZ(d)
})
# 结果
process    real 
 42.9ms  42.4ms 

bench::system_time(for ( i in 1:1000){
  table(d)
})
# 结果
process    real 
  107ms   106ms  
12345678910111213
```

在我的电脑上，果子老师的代码运行速度比R自带的table快了将近3倍。当然这是有原因的，因为R的table的代码功能更加复杂，能够比较多个变量之间的关系，例如`table(d,d)`。

既然是简单的统计每个元素的次数，那么我就想着能不能写出一个比果子老师速度更快的函数。 于是，我抽空写了下面的代码

```R
tableZG <- function(x){
  
  NA_pos <- is.na(x)
  NA_num <- sum(NA_pos)
  
  x <- x[!NA_pos]
  
  out <- vector(length = length(x))
  out_name <- rep(NA,  length(x))
  
  for (i in 1:length(x)) {
    
    for (j in 1:length(out_name)){
      if ( is.na(out_name[j]) ){
          out_name[j] <- x[i]
          out[j] <- 1
          break
        }
      
      if ( out_name[j] == x[i] ){
        out[j] <- out[j] + 1
        break
      } 
    }
  }
  
  if (NA_num > 0){
    na_end <- sum(!is.na(out_name))
    out_name[na_end + 1] <- 'NA'
    out[na_end + 1] <- NA_num
    
  } 
  na_pos <- is.na(out_name)
  out_name <- out_name[!na_pos]
  out <- out[!na_pos]
  names(out) <- out_name

  return(out)
  
}
12345678910111213141516171819202122232425262728293031323334353637383940
```

虽然我的代码更长了，但是并没有让速度提高，反而比果子老师的代码慢，甚至还不如R自带的table。

```R
system.time(for ( i in 1:1000){
  tableZG(d)
})
# 结果
process    real 
  148ms   148ms 
123456
```

当然那么一长串代码并不是白写的，因为我特意避免了使用R特有的内容，所以代码能够很容易改写成`C++`代码使用`Rcpp`调用，从而提高速度

新建一个`tableC.cpp`文件，代码内容如下

```R
#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
NumericVector tableC(CharacterVector cv){
  
  // initialize variable
  CharacterVector na = CharacterVector::create("NA");
  NumericVector out = rep(NumericVector::create(0), cv.size());
  CharacterVector out_name = rep(na, cv.size());
  int unique_num = 0;
  
  // 
  for (int i = 0; i < cv.size();i ++) {
    
    for (int j = 0; j < cv.size(); j++){
      
      if ( out_name[j] == "NA" ){
        out_name[j] = cv[i] ;
        out[j] = 1;
        unique_num += 1;
        break;
      }
      
      if ( out_name[j] == cv[i] ){
        out[j] = out[j] + 1;
        break;
      } 
    }
  }
 
  out.attr("names") = out_name;
  
  return out;
  
} 
123456789101112131415161718192021222324252627282930313233343536
```

然后在R里面用Rcpp这个C++代码，替换掉之前代码中的循环部分

```
Rcpp::sourceCpp("tableC.cpp")
tableZG <- function(x){
  
  NA_pos <- is.na(x)
  NA_num <- sum(NA_pos)
  
  x <- as.character(x[!NA_pos])
  res <- tableC(x)
  res <- res[!names(res) == "NA"]
  
  if (NA_num > 0){
    res <- c(res, "NA"=NA_num)
  }
  return(res)
}
123456789101112131415
```

于是这一次在C++的加持下，我写的table函数速度超过了果子老师的代码。

```
bench::system_time(for ( i in 1:1000){
  tableZG(d)
})
#结果
process    real 
 30.1ms  29.3ms 
123456
```

最后总结一下：如果一个操作只需要做一次，那么速度可能并不是最重要的。因为即便是一个原本要花24小时的代码，提速10倍，只要2小时，你可能也会愿意等一等。但是如果这个操作需要重复很多次，上百次，上千次，甚至上万次，那么你就可能等不下去了。你就需要对代码中的一些限速步骤进行优化，比如说table这种多功能函数，你就可以自己用R写一个简化版的函数，替换掉原先的代码。

如果对速度有更高的要求，那么就需要用到`C++`进行代码重写了。学习`C++`其实并不会特别难，因为有一个`Rcpp`简化了许多操作，你只需要掌握几个最基本的语言特性，比如说`C++`需要先定义变量才能使用变量。

## 推荐阅读

-   [给R使用者的C++最少必要知识](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Flinks.jianshu.com%2Fgo%3Fto%3Dhttp%253A%252F%252Fxuzhougeng.top%252Farchives%252FC%252B%252B_For_R_User)
-   [Rcpp学习笔记之Hello World!](https://app.yinxiang.com/OutboundRedirect.action?dest=https%3A%2F%2Flinks.jianshu.com%2Fgo%3Fto%3Dhttp%253A%252F%252Fxuzhougeng.top%252Farchives%252FWrite_first_function_Using_Rcpp)
