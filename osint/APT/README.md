Challenge Description

An alert just fired in your SOC. The system detected communication with IP address 185.210.219.250, which is associated with a known threat actor's C2 infrastructure. 

As the incident responder on call, your task is to:

1. Identify the APT group behind this IP address
2. Find their alternative designation/name
3. Determine their country of origin
4. Identify when they first became active
5. Determine the MITRE ATT&CK Technique ID for the initial access method used in this attack.
flag format: SECOPS{APTnumper_APTname_contry_year_MITRETechniqueID}
Example: If the answers were APT99, Shadow fox, Iran, 2007, and T1059, the flag is:
SECOPS{APT99_Shadow_Fox_Iran_2007_T1059}​

Author: YasseX

Step 1: Investigating the IP Address
The first step is to search the IP address on Google to identify which APT group is associated with it.

![Ip addresse](../images/apt2.png)

From the search results, we find that the IP address is linked to APT28.

Step 2: Gathering Information about APT28
Next, we search for APT28 to gather all the required information: alternative name, country, and first active year.

![wekipedia](../images/apt2.png)

From the results:

Alternative Designation: Fancy Bear

Country of Origin: Russia

First Active: 2004

Step 3: Finding the MITRE ATT&CK Technique ID
Finally, we search for the initial access method used by APT28.
APT28 commonly uses Phishing techniques.

By looking up in the MITRE ATT&CK framework, the technique ID for phishing is T1566.

Final Flag
Putting everything together in the correct format:

SECOPS{APT28_Fancy_Bear_Russia_2004_T1566}
