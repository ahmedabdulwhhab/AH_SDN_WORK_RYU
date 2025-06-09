const selectAction = document.getElementById("select-action");
const inputFields = document.getElementById("input-fields");
const confirmButton = document.getElementById("confirm");

selectAction.addEventListener("change", () => {
  const switch_id = document.getElementById("switch-select").value;
  const selectedOption = selectAction.value;
  if (selectedOption === "add-rule" || selectedOption === "block-traffic") {
    inputFields.innerHTML = `
      <label for="source-ip">Source IP:</label>
      <input type="text" id="source-ip" name="source-ip" placeholder="example: 10.0.0.1"><br>
      <label for="destination-ip">Destination IP:</label>
      <input type="text" id="destination-ip" name="destination-ip"  placeholder="example: 10.0.0.2"><br>
      <label for="pirority">pirority:</label>
      <input type="text" id="pirority" name="pirorityp" placeholder="example: 11"><br>
      <label for="protocol">Protocol:</label>
      <select id="protocol" name="protocol">
      <option value="TCP">TCP</option>
      <option value="UDP">UDP</option>
      <option value="ICMP">ICMP</option>
      <option value="ICMPv6">ICMPv6</option>
      <option value="IPV6">IPV6</option>
    </select>
    `;
  } else if (selectedOption == "delete-rule") {
    inputFields.innerHTML = `
            <label for="rule-id">Rule ID:</label>
            <input type="text" id="rule-id" name="rule-id">
            <br>
          `;
  } else {
    inputFields.innerHTML = "";
  }
});

confirmButton.addEventListener("click", () => {
  const selectedOption = selectAction.value;
  const switch_id = document.getElementById("switch-select").value;
  let api_url;
  if (selectedOption === "get-status") {
    api_url = "http://192.168.127.133:8085/firewall/module/status";
    fetch(
      "https://192.168.127.133:5000/send?api_url="+api_url+"&action=get_status",mode:'no-cors'
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "enable-firewall") {
    api_url = "http://192.168.127.133:8085/firewall/module/enable/000000000000000" + switch_id;
	fetch_url ="https://192.168.127.133:5000/send?api_url="+api_url+"&action=enable_firewall"
	//alert(api_url);
	alert(fetch_url);
	
	    let headers = new Headers();

  headers.append('Content-Type', 'application/json/image');
  headers.append('Accept', 'application/json');
  headers.append('Origin', 'https://192.168.127.133:5000');
  headers.append('Access-Control-Allow-Origin', 'https://192.168.127.133:5000');
  headers.append('Access-Control-Allow-Credentials', 'true');
    fetch(
      fetch_url,
      { method: "PUT" ,mode:'no-cors', headers: headers}
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "get-rules") {
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(`https://192.168.127.133:5000/send?api_url=${api_url}&action=get_rules`)
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "add-rule") {
    const sourceIp = document.getElementById("source-ip").value;
    const destinationIp = document.getElementById("destination-ip").value;
    const protocol = document.getElementById("protocol").value;
    const pirority = document.getElementById("pirority").value;
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=add_rule`,
      {
        method: "POST",mode:"no-cors",
        body: JSON.stringify({
          nw_src: sourceIp,
          nw_dst: destinationIp,
          nw_proto: protocol,
          pirority: pirority,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "block-traffic") {
    const sourceIp = document.getElementById("source-ip").value;
    const destinationIp = document.getElementById("destination-ip").value;
    const protocol = document.getElementById("protocol").value;
    const pirority = document.getElementById("pirority").value;
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=block_traffic`,
      {
        method: "POST",mode:"no-cors",
        body: JSON.stringify({
          nw_src: sourceIp,
          nw_dst: destinationIp,
          nw_proto: protocol,
          actions: "DENY",
          pirority: pirority,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "delete-rule") {
    const ruleId = document.getElementById("rule-id").value;

    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=delete_rule`,
      {
        method: "DELETE",mode:"no-cors",
        body: JSON.stringify({ rule_id: ruleId }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  }
});

//const selectAction = document.getElementById("select-action");
//const inputFields = document.getElementById("input-fields");
//const confirmButton = document.getElementById("confirm");

selectAction.addEventListener("change", () => {
  const switch_id = document.getElementById("switch-select").value;
  const selectedOption = selectAction.value;
  if (selectedOption === "add-rule" || selectedOption === "block-traffic") {
    inputFields.innerHTML = `
      <label for="source-ip">Source IP:</label>
      <input type="text" id="source-ip" name="source-ip" placeholder="example: 10.0.0.1"><br>
      <label for="destination-ip">Destination IP:</label>
      <input type="text" id="destination-ip" name="destination-ip"  placeholder="example: 10.0.0.2"><br>
      <label for="pirority">pirority:</label>
      <input type="text" id="pirority" name="pirorityp" placeholder="example: 11"><br>
      <label for="protocol">Protocol:</label>
      <select id="protocol" name="protocol">
      <option value="TCP">TCP</option>
      <option value="UDP">UDP</option>
      <option value="ICMP">ICMP</option>
      <option value="ICMPv6">ICMPv6</option>
      <option value="IPV6">IPV6</option>
    </select>
    `;
  } else if (selectedOption == "delete-rule") {
    inputFields.innerHTML = `
            <label for="rule-id">Rule ID:</label>
            <input type="text" id="rule-id" name="rule-id">
            <br>
          `;
  } else {
    inputFields.innerHTML = "";
  }
});

confirmButton.addEventListener("click", () => {
  const selectedOption = selectAction.value;
  const switch_id = document.getElementById("switch-select").value;
  let api_url;
  if (selectedOption === "get-status") {
    api_url = "http://192.168.127.133:8085/firewall/module/status";
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=get_status`
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "enable-firewall") {
    api_url = "http://192.168.127.133:8085/firewall/module/enable/000000000000000" + switch_id;
	
	api_url = "http://192.168.127.133:8085/firewall/module/enable/000000000000000" + switch_id;
	fetch_url ="https://192.168.127.133:5000/send?api_url="+api_url+"&action=enable_firewall"
	
	/*
	curl 'https://192.168.127.133:5000/send?api_url=http://192.168.127.133:8085/firewall/module/enable/0000000000000001&action=enable_firewall',
	
	
	curl ’http://192.168.127.133:8085/firewall/rules/0000000000000001’ \
--header "Content-Type: application/json" --data ’{"nw_src": "10.0.0.2/32","nw_dst": "10.0.0.1/32","nw_proto": "ICMP" ,"Auth" :"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.4zpj7GmQwAACrqo1DRhhdNsxcFVeNtU9RwEObRBIHM"}’

curl 'https://192.168.127.133:5000/send?api_url=http://192.168.127.133:8085/firewall/rules/0000000000000001' --header "Content-Type: application/json" --data '{"nw_src": "10.0.0.2/32","nw_dst": "10.0.0.1/32","nw_proto": "ICMP" ,"Auth" :"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.4zpj7GmQwAACrqo1DRhhdNsxcFVeNtU9RwEObRBIHM"}'
	
	*/
    let headers = new Headers();

  headers.append('Content-Type', 'application/json/image');
  headers.append('Accept', 'application/json');
  headers.append('Origin', 'https://192.168.127.133:5000');
  headers.append('Access-Control-Allow-Origin', 'https://192.168.127.133:5000');
  headers.append('Access-Control-Allow-Credentials', 'true');
    fetch(
      fetch_url,
      { method: "PUT" ,mode:'no-cors', headers: headers}
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "get-rules") {
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(`https://192.168.127.133:5000/send?api_url=${api_url}&action=get_rules`)
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "add-rule") {
    const sourceIp = document.getElementById("source-ip").value;
    const destinationIp = document.getElementById("destination-ip").value;
    const protocol = document.getElementById("protocol").value;
    const pirority = document.getElementById("pirority").value;
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=add_rule`,
      {
        method: "POST",mode:"no-cors",
        body: JSON.stringify({
          nw_src: sourceIp,
          nw_dst: destinationIp,
          nw_proto: protocol,
          pirority: pirority,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "block-traffic") {
    const sourceIp = document.getElementById("source-ip").value;
    const destinationIp = document.getElementById("destination-ip").value;
    const protocol = document.getElementById("protocol").value;
    const pirority = document.getElementById("pirority").value;
    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=block_traffic`,
      {
        method: "POST",mode:"no-cors",
        body: JSON.stringify({
          nw_src: sourceIp,
          nw_dst: destinationIp,
          nw_proto: protocol,
          actions: "DENY",
          pirority: pirority,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  } else if (selectedOption === "delete-rule") {
    const ruleId = document.getElementById("rule-id").value;

    api_url = `http://192.168.127.133:8085/firewall/rules/000000000000000${switch_id}`;
    fetch(
      `https://192.168.127.133:5000/send?api_url=${api_url}&action=delete_rule`,
      {
        method: "DELETE",mode:"no-cors",
        body: JSON.stringify({ rule_id: ruleId }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => showAlert(data));
  }
});

