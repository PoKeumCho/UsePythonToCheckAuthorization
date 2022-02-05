#!/bin/bash

# Generate deactivate.sh
echo '#!/bin/bash' > deactivate.sh
ps -ea | grep python | awk '{print $1}' | sed 's/^/kill /g' >> deactivate.sh
