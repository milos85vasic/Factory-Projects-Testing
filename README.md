# Factory Projects Testing
Testing 'Factory' projects like 'Apache Factory' or 'Mail Server Factory'.

## Supported projects
- [Mail Server Factory](https://github.com/milos85vasic/Mail-Server-Factory) - Support is under development
- [Apache Factory](https://github.com/milos85vasic/Apache-Factory) - Support is under development

## Remote server dependencies
- Curl

## How to use it:
TBD.

### Example configuration

```json
{
    "ssh": {
        "user": "root",
        "port": 7722,
        "host": "127.0.0.1"
    },
    "tests": [
        {
            "name": "Test 1",
            "type": "Mail-Server-Factory",
            "configuration": {
                
            }
        }
    ]
}
```

