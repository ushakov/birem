Hi {{user}},

Here are your birthday reminders for {{date.month}} {{date.day}}, {{date.year}}:

{% if today %}Today: {{today.note}} {% if today.age %}({{today.age}} years){% endif %}

{% endif %}{% for rem in reminders %}{{rem.weekday}} {{rem.month}} {{rem.day}}: {{rem.note}} {% if rem.age %}({{rem.age}} years){% endif %}
{% endfor %}