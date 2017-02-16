(define cons (lambda (x y) (lambda (m) (m x y))))
(define car (lambda (z) (z (lambda (p q) p))))
(define cdr (lambda (z) (z (lambda (p q) q))))

(define listprint
  (lambda (l)
    (map (lambda (x) (print x)) l)))

(define identity (lambda (x) x))
(define positive? (lambda (x) (> x 0)))
(define negative? (lambda (x) (< x 0)))
(define even? (lambda (x) (= 0 (% x 2))))
(define odd? (lambda (x) (! (even? x))))
(define xor (lambda (x y) (and (or x y) (not (and x y)))))
(define nor (lambda (x y) (not (or x y))))
(define nand (lambda (x y) (not (and x y))))
(define >= (lambda (x y) (or (> x y) (= x y))))
(define <= (lambda (x y) (or (< x y) (= x y))))

(define repeat (lambda (token number)
  (if (= number 0)
      list
      (cons
       token
       (repeat token (- number 1))))))

(define pow (lambda (b e) (reduce (lambda (a b) (* a b)) (repeat b e))))
(define range (lambda (a b) (if (>= a b) (list) (cons a (range (+ a 1) b)))))
(define do (lambda () (last ...)))


(define map
  (lambda (f l)
    (if (none? (car l))
        None
        (cons (f (car l)) (map f (cdr l))))))

(define foreach
  (lambda (f l)
    (do
        (f (car l))
        (if (none? (cdr l))
         None
         (foreach f (cdr l))))))

(define filter
  (lambda (f l)
    (if (none? (car l)) l
        (if (f (car l))
            (cons (car l) (filter f (cdr l)))
            (filter f (cdr l))))))

(define reduce
  (lambda (f l)
    (if (none? (car l))
        None
        (if (none? (cdr l))
            (car l)
            (f
             (car l)
             (reduce f (cdr l)))))))
