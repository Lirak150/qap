# Алгоритмы исследования операций, лабораторная работа 4

## ТЗ:

Реализовать и сравнить алгоритмы для решения quadratic assignment problem.

1. Local search - сделать либо с best-improvement либо first-improvement + don't look bits (был выбран best improvement).
2. Iterated local search ИЛИ Guided local search (был выбран iterated local search).

## Структура файлов

- algos/local_search.py - реализация алгоритмов
- tests - тесты для задач и их парсинг.
- solutions/local_search - решения для local search
- solutions/iterated_local_search - решения для Iterated local search

## Результаты

### Local Search

|      |    tai20a |      tai40a |      tai60a |      tai80a |     tai100a |
|:-----|----------:|------------:|------------:|------------:|------------:|
| time |      0.17 | 0.72        | 1.7         | 3.1         | 5.1         |
| cost | 916746    | 3.79672e+06 | 8.65503e+06 | 1.57586e+07 | 2.40115e+07 |

### Iterated Local Search

|      |   tai20a |       tai40a |        tai60a |        tai80a |       tai100a |
|:-----|---------:|-------------:|--------------:|--------------:|--------------:|
| time |      7.8 | 73           | 150           | 280           | 550           |
| cost | 803898   |  3.53487e+06 |   8.13174e+06 |   1.50045e+07 |   2.33805e+07 |