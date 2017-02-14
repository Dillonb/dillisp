(define a (cons 1 (cons 2 (cons 3 None))))
(defn double (x) (* 2 x))
(define b (lmap double a))
(lforeach (lambda (x) (print x)) b)
