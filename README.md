# **Gene_Ontology_2nd_Level**

Gene_Ontology_2nd_Level is a program that returns a Gene Ontology at 2nd level from any query. Usually a query is an output exported file from Blast2Go.

---

## RELEASE

Version 1.0.0 - Mar 15, 2019.

Available from <https://github.com/oseias-r-junior/Gene_Ontology_2nd_Level>. 

---

## REQUIREMENTS

Gene_Ontology_2nd_Level runs on Python 3.4+ and has been tested on Ubuntu 18.04. It should work on any modern GNU/Linux distro. No installation for this program is required. However, since it works on outputs from other software, it is necessary to have access to such software in order to be able to use this program adequately.
For convenience, after downloading and extracting the latest Gene_Ontology_2nd_Level release from GitHub you can move the extracted directory to the desired destination.
>**Note**: Older or newer versions of the program Blast2Go as well as other operating systems might also work, but since they have not been tested this is not guaranteed.

---

## USAGE

`python go_to_2nd.py <file>`

In order to run Gene_Ontology_2nd_Level, indicate the input file you wish to process

**Example**: `python go_to_2nd.py Escherichia\_coli\_K12.txt` 

---

## RESULTS

Gene_Ontology_2nd_Level will output a comma-separated values table for Excel (a .csv file).

---

## CITATION

If you find this software useful in your research, please cite the following references according to the programs you use:

- Dourado, Manuella Nóbrega; Pierry, Paulo M.; Feitosa-Junior, Oseias Rodrigues; Uceda, G.; Zaini, Paulo A.; Dandekar, Abhaya M.; da Silva, Aline M.; Araújo, Welington Luiz. 
Methylobacterium mesophilicum endophyte inhibits Xylella fastidiosa pathogen: physiological and molecular focus. (draft).

- Ashburner M, Ball CA, Blake JA, et al. Gene ontology: tool for the unification of biology. 
The Gene Ontology Consortium. Nat Genet. 2000;25(1):25-9.

---

## ISSUES AND REQUESTS

If you experience any issues or would like to see support for an additional feature implemented in Gene_Ontology_2nd_Level, please file a request in the GitHub issue tracker or email it to the developer. Feel free to contact the developer with any further questions regarding this software. You can reach him at mail to: oseias.rf.junior@gmail.com.

---

## LICENSES

Copyright © 2019 Guillermo Uceda | Oseias Feitosa-Junior

This program is a free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

The dataset included with this program is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/.
