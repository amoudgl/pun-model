# Computational Model for Linguistic Humor in Puns

This is a clean python implementation of computational model for puns. The model employs a probabilistic framework to compute two measures, namely ambiguity and distinctiveness, upon which a regression model is fit to generate funniness ratings.

If you find this code useful in your research or want to learn more about the model, please refer to:

```
@article{kao2016computational,
  title={A computational model of linguistic humor in puns},
  author={Kao, Justine T and Levy, Roger and Goodman, Noah D},
  journal={Cognitive science},
  volume={40},
  number={5},
  pages={1270--1285},
  year={2016},
  publisher={Wiley Online Library}
}
```

## Experiments

Author's original implementation can be found here: [[justinek/pun-paper](https://github.com/justinek/pun-paper)]. This implementation reproduces the results in the paper and I obtain exactly the same ambiguity and dinstictiveness values as there in original result csv sheet `data-agg.csv` (received from author).

However, I noticed [several issues](v2#issues-in-v0) in the original relatedness and unigram data used by author to compute measures. I also found some bugs in the original implementation. Thus, I performed a series of experiments to fix them which I dubbed in this repository as `v0`, `v1` and `v2`.

> **[`v0`](./v0)**: Author's original implementation.   
> **[`v1`](./v1)**: Neat re-implementation of `v0` (also compatible with python3).   
> **[`v2`](./v2)**: Built on top of `v1`. Fixes `v0` data issues and implementation bugs.   


Following is a concise table representing different models:

|         | `v0`  | `v1`  | `v2` |
| ------------- |:-------------:| -----:| -----:|
| Reproduces paper results | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:|
| Python3 compatible | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Uses correct data | :x: | :x: | :heavy_check_mark: |
| Uses correct model | :x:| :x: | :heavy_check_mark: |


### Note


:arrow_forward: *Please use the final version [`v2`](./v2) if you wish to reproduce the correct puns model or adapt it for further research.*

:arrow_forward: *Additional notes, introductions to run code and results of each version can be found in its respective directory.*

## Acknowledgements

- [[justinek/pun-paper](https://github.com/justinek/pun-paper)] served as an important reference. Most of the data and `v0` scripts were borrowed from it.
- Thanks to the authors, Justine Kao and Noah Goodman, for their help.

## License

BSD
