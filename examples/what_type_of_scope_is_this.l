(define make-test
    (lambda ()
        (do
            (define x 'lexical)
            (lambda ()
                x))))

(define f (make-test))

(define x 'dynamic)
(print (f))
