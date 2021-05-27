export GOPROXY ?= https://goproxy.cn

default:
	go run main.go blockchain.go block.go pow.go utils.go utxo.go merkle_tree.go \
		transaction.go transaction_in.go transaction_out.go cli.go wallet.go wallets.go \
		base58.go server.go

build:
	go build -o blockchain main.go blockchain.go block.go \
		pow.go utils.go cli.go transaction.go transaction_in.go transaction_out.go wallet.go wallets.go \
		utxo.go merkle_tree.go server.go \
		base58.go