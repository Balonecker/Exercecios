package javaapplication4;

public class Complex {
    
    private double a;
	private double b;
	
	public Complex (double a, double b) {
	    this.a = a; this.b = b;
	}
	
	public Complex () {
	    this.a = 0.0; this.b = 0.0;
	}
	
	public static Complex somar (Complex x, Complex y) {
	    return new Complex (x.a + y.a, x.b + y.b);
	}
	
	public static Complex subtrair (Complex x, Complex y) {
	    return new Complex (x.a - y.a, x.b - y.b);
	}
	
    public String toString() {
	    return "(" + a + ", " + b + ")";
	}
}
class TesteComplex {
    public static void main (String[] args) {
	    Complex abc = new Complex (7.9, 8.2 );
		Complex def = new Complex (9.3, -4.1);
	    Complex zero = new Complex();
		System.out.println ("Resultado ABC:" + abc); 
		System.out.println ("Resultado DEF:" + def); 
		System.out.println ("Resultado ABC+DEF:" + Complex.somar (abc, def)); 
		System.out.println ("Resultado ABC-DEf:" + Complex.subtrair (abc, def)); 
	}
}