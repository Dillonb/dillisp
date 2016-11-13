(define positive? (lambda (x) (> x 0)))
(define negative? (lambda (x) (< x 0)))
(define even? (lambda (x) (= 0 (% x 2))))
(define odd? (lambda (x) (! (even? x))))
