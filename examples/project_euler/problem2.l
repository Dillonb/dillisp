(taildefn fib-seq-iter (a b n acc)
    (if (= n 0)
        acc
        (fib-seq-iter (+ a b) a (- n 1) (append acc a))))

(defn fib-seq (n) (fib-seq-iter 1 0 n (list)))

(print (reduce (lambda (a b) (+ a b)) (filter even? (fib-seq 33))))


;;; Not used, here for reference
(taildefn fib-iter (a b n)
    (if (= n 0)
        b
        (fib-iter (+ a b) a (- n 1))))

;;; Not used, here for reference
(defn fib (n) (fib-iter 1 0 n))
