from pickletools import optimize
import pandas as pd
import torch
import torch.nn as nn
from torch.nn import MSELoss
from torch.utils.data import Dataset, DataLoader

class SequentialDataset(Dataset):

    def __init__(
        self,
        path_to_ts_data:str,
        top_name:str,
        date_col_name:str,
        sequence_length:int,
        pred_length:int
    ) -> None:
        super(SequentialDataset,self).__init__()

        self.time_series_df = pd.read_csv(
            path_to_ts_data,
            low_memory=False,
            usecols=[top_name,date_col_name],
            parse_dates=[date_col_name]
        )
        self.sequence_length = sequence_length
        self.pred_length = pred_length
        self.time_series_tensor = torch.FloatTensor(self.time_series_df[top_name].values).unsqueeze(dim=1)

    
    def __len__(self):
        return len(self.time_series_tensor)-self.sequence_length - self.pred_length + 1

    def __getitem__(self, index):
        
        train_series  = self.time_series_tensor[index:index+self.sequence_length]
        test_series = self.time_series_tensor[index+self.sequence_length]

        return {
            'train' : train_series, 
            'test' : test_series
        }


class LSTMModule(nn.Module):
    
    def __init__(
        self,
        input_size=1,
        hidden_size=2,
        output_size=1,
        num_layers=2,
        batch_first=True) -> None:
        super(LSTMModule,self).__init__()

        self.input_size=input_size
        self.hidden_size=hidden_size
        self.num_layers=num_layers
        self.batch_first=batch_first
        self.output_size=output_size

        self.lstm_module = nn.LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=True
        )
        self.linear_module = nn.Linear(
            in_features=self.hidden_size,
            out_features=self.output_size
        )

    def forward(self,x):

        batch_size = x.shape[0]
        

        h_cell = torch.zeros(self.num_layers,batch_size,self.hidden_size).requires_grad_()
        c_cell = torch.zeros(self.num_layers,batch_size,self.hidden_size).requires_grad_()

        _,(h_out,_) = self.lstm_module(x,(h_cell,c_cell))

        prediction = self.linear_module(h_out[0])

        return prediction

def train_model(train_data_loader,model,optimizer,loss_func):

   
    total_loss = 0
    total_batch = len(train_data_loader)

    for  i,batch in enumerate(train_data_loader):

        optimizer.zero_grad()

        # print('train batch ' ,batch['train'].shape)
        x = model(batch['train'])
        loss = loss_func(x,batch['test'])
        
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / total_batch
    print(f'average loss: {avg_loss}')

if __name__ == '__main__':

    dataset = SequentialDataset(
        path_to_ts_data='./solutions/datasets/trends1.csv',
        top_name='top 1',
        date_col_name='date',
        sequence_length=4,
        pred_length=1
    )

seq_data_loader = DataLoader(dataset=dataset,batch_size=1,num_workers=5)
model = LSTMModule()
loss_func = MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)

for i in range(2000):
    train_model(seq_data_loader,model,optimizer,loss_func)

