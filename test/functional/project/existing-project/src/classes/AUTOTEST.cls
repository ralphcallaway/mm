public with sharing class AUTOTEST {

	String someString;
	public String myPublicString { get; set; }

	public AUTOTEST(String foo , Boolean bar) {
		ApexPages.StandardController c;
		c.cancel();
	}

	void doSomething() {
		String f = 'foo';
		f.capitalize();
		for (Integer i=0; i < 5; i++) {
			Account a = new Account();
			a.AccountSource = 'foo';
			insert a;
			String s = 'foo';
			
		}
	}
}