<br>
In The Name of Allah, <br>
in this project, two simple switches layer 2 are configured (datapath id is 1 and 2) <br>
router datapath id is 33 (hex 21) <br>
<firewall datapath id is 49 (hex 31) <br>
we modify official firewall_rest by adding if condition to run firewall only on dp.id == 49 <br>
also do same for router dp.id == 33 <br>
also for simple switch. <br>
so we created a custom controller for Router, firewall and simple switch layer 2 <br>
for this link on youtube for more
https://youtu.be/gIoki9wpsqw
    <br>
    h1 can ping h2 h3 <br>
    h2 can ping h1 h4 <br>
    h3 can ping h1 h4 <br>
    h4 can ping h2 h3 <br>
