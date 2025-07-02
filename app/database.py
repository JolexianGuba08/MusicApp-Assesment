from supabase import create_client, Client

url: str = "https://tishttlwavnrzcquybbh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRpc2h0dGx3YXZucnpjcXV5YmJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzNzUwOTIsImV4cCI6MjA2Njk1MTA5Mn0.uIJ7tvPdDQaE1LYw2HYj0b1X4tT2ZjIcZiq-X9FoAXw"
supabase: Client = create_client(url, key)
