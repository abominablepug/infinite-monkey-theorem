<script lang="ts">
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';

	let popupOpen = $state(false);
	let typedText = $state("");
	let status = $state("Disconnected");
	let tokens = $state<{ text: string, timestamp: string }[]>([]);
	let hoveredToken = $state<{ text: string, timestamp: string } | null>(null);
	let sortMethod = $state('order');
	let sortAscending = $state(true);
	let filterText = $state('');
	let collapseDuplicates = $state(false);
	let activeTime = $state(0.0);

	let formattedTime = $derived.by(() => {
		const totalSeconds = Math.floor(activeTime);
		const hours = Math.floor(totalSeconds / 3600);
		const minutes = Math.floor((totalSeconds % 3600) / 60);
		const seconds = totalSeconds % 60;
		return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
	})

	let modifiedTokens = $derived.by(() => {
		let list = [...tokens];
		if (sortMethod === 'order') {
			list = list;
		} else if (sortMethod === 'length') {
			list.sort((a, b) => b.text.length - a.text.length);
		} else if (sortMethod === 'alphabetical') {
			list.sort((a, b) => a.text.localeCompare(b.text));
		}

		if (!sortAscending) list.reverse();

		if (filterText.trim() !== '') {
			list = list.filter(token => token.text.toLowerCase().includes(filterText.toLowerCase()));
		}

		if (collapseDuplicates) {
			const counts = new Map<string, number>();
			const uniqueList: { text: string, count: number }[] = [];

			for (const word of list) {
				const count = counts.get(word.text) || 0;
				if (count === 0) {
					uniqueList.push({ text: word.text, count: 1 });
				}
				counts.set(word.text, count + 1);
			}

			return uniqueList.map(word => ({
				...word,
				count: counts.get(word.text) || 1
			}));
		}

		return list.map(word => ({ ...word, count: 1 }));
	})

	let socket: WebSocket;

	onMount(() => {
		const socketUrl = env.PUBLIC_BACKEND_URL;
		socket = new WebSocket(socketUrl);

		socket.onmessage = (event) => {
			try {
				const data = JSON.parse(event.data);

				if (data.type === 'history') {
					typedText = data.letters;
					tokens = data.words;
				} else if (data.type === 'word') {
					typedText += " ";
					tokens.push(data);
				} else if (data.type === 'letter') {
					typedText += data.text;
					if (typedText.length > 5000) typedText = typedText.slice(-5000);
				}
				activeTime = data.active_time || activeTime;
			} catch (e) {
				console.error("Error parsing message:", e);
			}
		};

		socket.onopen = () => {
			status = "Connected";
		};
		socket.onclose = () => {
			status = "Disconnected";
		};
	});

	const toggle = (cmd: string) => {
		if (socket && socket.readyState === WebSocket.OPEN) {
			socket.send(cmd);
		}
	};

</script>

<main class="min-h-screen bg-slate-950 text-slate-200 p-8 font-mono">
	<div class="max-w-4xl mx-auto space-y-6">
		<header class="flex justify-between items-center border-b border-slate-800 pb-4">
			<h1 class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-purple-600 bg-clip-text text-transparent">
				Infinite Monkey Theorem
			</h1>
			<div class="flex items-center gap-2 mt-1">
				<span class="text-[10px] text-slate-500 uppercase tracking-tighter">Total Runtime:</span>
				<span class="text-xs font-bold text-cyan-500 tabular-nums">{formattedTime}</span>
			</div>
			<div class="flex items-center gap-2">
				<div class="w-3 h-3 rounded-full {status === "Connected" ? "bg-emerald-500 animate-pulse" : "bg-red-500"}"></div>
				<span class="text-sm font-medium uppercase tracking-widest">{status}</span>
			</div>
		</header>

		<div class="flex flex-wrap gap-3">
			<button onclick={() => toggle('start')} class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-md transition-colors font-bold text-slate-950">
				Give Typewriter to Monkey 🐵
			</button>
			<button onclick={() => toggle('stop')} class="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-md transition-colors">
				Take Typewriter Away 🙊
			</button>
			<button onclick={() => popupOpen = true} class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-md transition-colors">
				Show Found Words ({tokens.length}) 🙈
			</button>
			<button onclick={() => { typedText = ""; }} class="px-4 py-2 border border-slate-700 hover:bg-slate-800 rounded-md transition-colors">
				Reset 🙉
			</button>
		</div>

		<div class="relative bg-black rounded-xl border border-slate-800 p-6 shadow-2xl h-96 overflow-y-auto break-all scrollbar-thin scrollbar-thumb-slate-800">
			<div class="text-emerlad-500/80 leading-relaxed">
				{typedText}
				<span class="inline-block w-1 h-4 bg-emerald-500 animate-pulse ml-1"></span>
			</div>
		</div>

		<footer class="mt-8 pt-6 border-t border-slate-800/50 flex flex-col items-center justify-center text-sm text-slate-500 gap-2">
			<p>
				Made by 
				<a href="https://github.com/abominablepug" target="_blank" rel="noopener noreferrer" class="text-purple-400 hover:text-purple-300 transition-colors font-medium">
					abominablepug
				</a>
			</p>
			<a href="https://github.com/abominablepug/infinite-monkey-theorem" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 hover:text-slate-300 transition-colors text-xs group">
				<svg class="w-4 h-4 opacity-70 group-hover:opacity-100 transition-opacity" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
					<path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
				</svg>
				github.com/abominablepug/infinite-monkey-theorem
			</a>
		</footer>

		{#if popupOpen}
			<div class="fixed inset-0 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4 z-50">
				<div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col">
					
					<div class="p-6 border-b border-slate-800">
						<div class="flex justify-between items-center mb-6">
							<h2 class="text-xl font-bold text-cyan-400">Words Discovered</h2>
							<button onclick={() => popupOpen = false} class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-800 hover:bg-red-900/40 hover:text-red-400 transition-all text-slate-400">✕</button>
						</div>

						<div class="flex flex-col md:flex-row gap-3">
							<div class="relative flex-grow">
								<span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">FIND:</span>
								<input 
									type="text" 
									placeholder="..." 
									bind:value={filterText} 
									class="w-full bg-black/40 border border-slate-700 rounded-lg pl-14 pr-4 py-2 text-cyan-500 placeholder-slate-700 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 transition-all font-mono"
								/>
							</div>

							<div class="flex items-center bg-black/40 border border-slate-700 rounded-lg px-2">
								<select 
									bind:value={sortMethod}
									class="bg-transparent text-slate-400 text-xs py-2 focus:outline-none cursor-pointer hover:text-cyan-400"
								>
									<option value="order">Sequence</option>
									<option value="length">Length</option>
									<option value="alphabetical">A-Z</option>
								</select>

								<div class="w-[1px] h-4 bg-slate-700 mx-2"></div>

								<button 
									onclick={() => sortAscending = !sortAscending}
									class="text-[10px] font-black px-2 py-1 rounded transition-colors {sortAscending ? 'text-cyan-400 bg-cyan-400/10' : 'text-purple-400 bg-purple-400/10'}"
								>
									{sortAscending ? 'ASC ▲' : 'DESC ▼'}
								</button>

								<div class="w-[1px] h-4 bg-slate-700 mx-2"></div>
								<button 
									onclick={() => collapseDuplicates = !collapseDuplicates}
									class="text-[10px] font-black px-2 py-1 rounded transition-colors {collapseDuplicates ? 'text-emerald-400 bg-emerald-400/10' : 'text-slate-500 bg-slate-800'}"
									title="Collapse Duplicates"
								>
									{collapseDuplicates ? 'UNIQUE' : 'DUPES'}
								</button>
							</div>
						</div>
					</div>

					<div class="p-6 overflow-y-auto flex flex-wrap gap-2 custom-scrollbar min-h-[200px] content-start">
						{#if modifiedTokens.length === 0}
							<div class="w-full py-12 text-center">
								<p class="text-slate-600 italic">No patterns match current filter.</p>
							</div>
						{:else}
							{#each modifiedTokens as token}
								<button 
									onmouseenter={() => hoveredToken = token}
									onmouseleave={() => hoveredToken = null}
									class="group px-3 py-1.5 bg-slate-800/30 border border-slate-800 hover:border-cyan-500/50 rounded-md transition-all"
								>
									<span class="text-slate-300 group-hover:text-cyan-400">{token.text}</span>
									{#if token.count > 1}
										<span class="ml-1 text-[10px] font-black text-emerald-500">×{token.count}</span>
									{/if}
								</button>
							{/each}
						{/if}
					</div>

					<div class="px-6 py-2 bg-black/40 border-t border-slate-800/50 h-10 flex items-center">
						{#if hoveredToken}
							<div class="flex items-center gap-4 animate-in fade-in slide-in-from-left-2 duration-200">
								<span class="text-[10px] text-slate-500 uppercase font-bold">Selected:</span>
								<span class="text-xs text-cyan-400 font-bold">"{hoveredToken.text}"</span>
								<span class="text-[10px] text-slate-600">—</span>
								<span class="text-[10px] text-slate-500 uppercase font-bold">Found at:</span>
								<span class="text-xs text-emerald-500 tabular-nums">{hoveredToken.timestamp}</span>
							</div>
						{:else}
							<span class="text-[10px] text-slate-600 italic">Hover a word to see discovery details...</span>
						{/if}
					</div>

					<div class="p-4 bg-black/20 border-t border-slate-800 flex justify-between items-center rounded-b-2xl">
						<span class="text-[10px] text-slate-500 uppercase">Visible: {modifiedTokens.length} / Total: {tokens.length}</span>
						<button onclick={() => popupOpen = false} class="px-6 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm rounded-md transition-colors border border-slate-700">
							Exit
						</button>
					</div>
				</div>
			</div>
		{/if}
	</div>
</main>

<style>
.scrollbar-thin::-webkit-scrollbar {
	width: 8px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
	background: #1e293b;
	border-radius: 10px;
}
</style>
