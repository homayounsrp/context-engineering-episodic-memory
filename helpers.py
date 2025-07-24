template = """Ticket Subject: {subject}
Ticket From: {from_email}
Ticket Description: 
```
{description}
```
> Triage Result: {result}"""

def format_few_shot_examples(examples):
    strs = ["Here are some previous examples:"]
    for eg in examples:
        strs.append(
            template.format(
                subject=eg.value["ticket"]["subject"],
                from_email=eg.value["ticket"]["from"],
                description=eg.value["ticket"]["ticket_description"][:400],
                result=eg.value["label"],
            )
        )
    return "\n\n------------\n\n".join(strs)