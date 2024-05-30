# bf1-login
A login service for the beaverf1 site, for se1@OSU

### !!! Security note:
This is not the safest way to run a login service. I need something to meet a deadline and be minimumly viable, secure functionality comes later. This code comes with no warranty and should not be used outside of the BF1 project, at least for now. Here be dragons.

Request schema:

```json
{user:name,pass:word}
```