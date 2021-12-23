<template>
<div class="app-container">
  <!-- 搜索表单 -->
    <el-form
      ref="queryParams"
      :model="queryParams"
      size="small"
      :inline="true"
    >
      <el-form-item>
        <!-- <el-button type="success" icon="el-icon-edit" :disabled="single" @click="handleUpdate">修改</el-button> -->
        <el-button
          type="danger"
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          >删除</el-button
        >
      </el-form-item>
      <el-form-item prop="report_name">
        <el-input
          v-model="queryParams.planname"
          placeholder="报告名称"
          clearable
          style="width: 220px"
          @keyup.enter.native="showReport"
        />
        <el-input
          v-model="queryParams.taskname"
          placeholder="任务名称"
          clearable
          style="width: 220px"
          @keyup.enter.native="showReport"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showReport">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading"
              :data="reportList"
              border  
              @selection-change="handleSelectionChange"           
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column prop="report_name" label="报告名称" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.report_name }} </template>
      </el-table-column>
      <el-table-column prop="data" label="日期" min-width="60">
      <template slot-scope="scope"> {{ split_time(scope.row.fields.report_name) }} </template>
      </el-table-column>
      <el-table-column prop="case_num" label="案例数" min-width="40">
      <template slot-scope="scope"> {{ scope.row.fields.case_num }} </template>
      </el-table-column>
      <el-table-column prop="pass_num" label="通过数" min-width="40">
      <template slot-scope="scope"> {{ scope.row.fields.pass_num }} </template>
      </el-table-column>
      <el-table-column prop="fail_num" label="失败数" min-width="40">
      <template slot-scope="scope"> {{ scope.row.fields.fail_num }} </template>
      </el-table-column>
      <el-table-column prop="error_num" label="错误数" min-width="40">
      <template slot-scope="scope"> {{ scope.row.fields.error_num }} </template>
      </el-table-column>
      <el-table-column prop="task_name" label="任务名称" min-width="80">
      <template slot-scope="scope"> {{ get_map_task(scope.row.fields.task) }} </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="110">
        <template slot-scope="scope">
            <el-button
            type="primary"
            size="mini"
            round
            plain
            @click.stop="queryReport(scope.row.pk)"
          >查看报告</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="sc-pagination-container">
     <ul >
      <el-pagination
        background
        layout="total,prev, pager, next"
        v-show="pagination.total>0"
        :total="pagination.total"
        :page-size="pagination.limit"
        @current-change="handleCurrentChange">
      </el-pagination>
     </ul>
 </div>   
  </div>
</template>
<script>
import {getreport,del} from '@/api/report';
import {get_task} from '@/api/task'
export default {
  // name: 'test1',
  data () {
    return {
      reportList: [],
      loading: false,
      //默认非多选时【删除】按钮不可点
      multiple:true,
      //多选
      report_ids:[],
      options: [],
      queryParams: {
          planname: undefined,
          taskname:undefined
        },
      pagination: {
          page: 1,
          limit: 5,
          total: 0
        },
    }
  },
  mounted: function () {
    this.showReport()
    this.gettask()
  },
  methods: {
    showReport () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getreport(this.queryParams).then((response) => {
            this.reportList = response.data.data
            this.pagination.total=response.data.totalCount
        })
    },
    gettask(){
        get_task().then((response)=>{
            this.options=response.data
        })
    },
    get_map_task(parm){
        let label=""
        this.options.forEach(item=>{
            if(item.taste_id===parm){
                label=item.taste_name
            }
        })
        return label
    },
    handleReset() {
        this.pagination = {
          page: 1,
          limit: 5,
          total: 0
        }
        this.queryParams = {
          planname: undefined,
          taskname:undefined
        }
        this.showReport()
      },
    handleDelete(report_ids) {
        if(this.report_ids.length>0){
          report_ids=this.report_ids
      }
        this.$confirm('确认删除该项目?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          del(report_ids).then(() => {
            this.$message.success('删除成功')
            this.showReport()
          })
        }).catch(() =>
          this.$message.info('已取消删除')
        )
      },
      //列表多选操作
    handleSelectionChange(selection){
        this.report_ids=selection.map(item=>item.pk)
        this.multiple=selection.length === 0
    },
     handleCurrentChange(val) {
      this.pagination.page = val;
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      getreport(this.queryParams).then((response) => {
            this.reportList = response.data.data
            this.pagination.total=response.data.totalCount
      });
    },
      split_time(data){
            return data.split("-")[1].slice(0,10)
      },
      queryReport(row_id){
        const flag="report"
        this.$router.push({path:'/get_report',query:{flag:flag,id:row_id}})
      }

  },
  components:{
    
  }

}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }


  ul {
  list-style-type: none;
  padding: 0;
}


li {
  /* display: inline-block; */
  margin: 0 5px;
}


a {
  color: #42b983;
}
</style>



