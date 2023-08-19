<h3 align="center">TraderPlus FileDiffLogger</h3>















</div>































<!-- ABOUT THE PROJECT -->







## About The Project



<h3 align="center">Overview:</h3> 
This Python script serves the purpose of comparing the contents of two files: TraderPlusPriceConfig.json and Types.xml.
It generates two separate logs that highlight discrepancies between the two files. These logs are saved in the \downloads directory.


 <br />1. missing_in_types_log.txt: This log documents items that are absent in Types.xml but are present in TraderPlusPriceConfig.json.
 <br />2. missing_in_trader_log.txt: This log records items that are absent in TraderPlusPriceConfig.json but exist in Types.xml.

Additionally, the script attempts to create placeholder versions of types.xml and \TraderPlusPriceConfig.json. 
These placeholder files can be used as templates for incorporating actual code. However, it's essential to edit these files before using them. 
They shouldn't be directly copied and pasted into projects without proper modifications.

The purpose of this script is to facilitate the identification of inconsistencies between the two mentioned files and to help create basic template files and prevent items spawning which can't be sold, or trader items being sold which aren't in types.


<h3 align="center">License:</h3> 
General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)












<p align="right">(<a href="#readme-top">back to top</a>)</p>




















