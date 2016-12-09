(taildefn fib-seq-iter (a b predicate acc)
    (if (not (predicate a))
        acc
        (fib-seq-iter (+ a b) a predicate (append acc a))))

(defn fib-seq (predicate) (fib-seq-iter 1 0 predicate (list)))

(defn under-4-million (n) (< n 4000000))

(print (reduce (lambda (a b) (+ a b)) (filter even? (fib-seq under-4-million))))
