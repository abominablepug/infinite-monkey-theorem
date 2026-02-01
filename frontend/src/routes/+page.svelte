<script lang="ts">
	import { onMount } from 'svelte';

	let socket: WebSocket;
	let typedText = '';
	let status = "Disconnected";

	onMount(() => {
		socket = new WebSocket('ws://localhost:8000/ws');

		socket.onmessage = (event) => {
			typedText += event.data;
		};

		socket.onopen = () => {
			status = "Connected";
		};
		socket.onclose = () => {
			status = "Disconnected";
		};
	});

	const toggle = (cmd: string) => socket.send(cmd);
</script>

<main>
	<h1>Infinite Monkey Dashboard</h1>
	<p>Status: {status}</p>

	<div>
		<button on:click={() => toggle('start')}>Start Typing</button>
		<button on:click={() => toggle('stop')}>Stop Typing</button>
		<button on:click={() => typedText = ""}>Reset</button>
	</div>

	<div>{typedText}</div>
</main>
