(define fib (memoized-lambda n (if (or (= n 0) (= n 1)) n (+ (fib (- n 1)) (fib (- n 2))))))
(print (map fib (range 1 50)))